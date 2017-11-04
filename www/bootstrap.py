import boto3
from boto3.dynamodb.conditions import Key, Attr
import jinja2
import json

DDB_RESOURCE = boto3.resource('dynamodb')
S3_CLIENT = boto3.client('s3', region_name="eu-west-1")

ddb_device_table_name = "iowt-devices"
ddb_event_table_name = "iowt-events"
ddb_device_table = DDB_RESOURCE.Table(ddb_device_table_name)
ddb_event_table = DDB_RESOURCE.Table(ddb_event_table_name)

s3_bucket = "iowt"

owner = "chrisw"
email_address = "test@test.test"
isAdmin = True

api_url = "http://localhost:8000"


def render_s3_template(client, bucket, template_name, content=None):
    # If no conent is supplied, set to empty dict
    if content is None:
        content = dict()

    file_object = client.get_object(Bucket=bucket, Key=template_name)
    file_content = file_object['Body'].read().decode('utf-8')
    rendered_html = jinja2.Environment().from_string(file_content).render(content)

    return(rendered_html)



# Admin - Loop through devices
things = list()
response = ddb_device_table.scan()
for item in response['Items']:
    things.append(item)

with open("s3/admin.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "admin.tmpl",
                                      {"devices": things,
                                       "isadmin": isAdmin,
                                       "icon_path": "Things",
                                       "username": owner})
    html_file.write(file_content)


# Loop through devices and pick all tagged with 'owner'
things = list()
response = ddb_device_table.scan(FilterExpression=Attr('deviceOwner').eq(owner))
for item in response['Items']:
    things.append(item)

with open("s3/mythings.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "mythings.tmpl",
                                      {"devices": things,
                                       "isadmin": isAdmin,
                                       "apiurl": api_url,
                                       "icon_path": "Things",
                                       "username": owner})
    html_file.write(file_content)


# loop devices and get events
events = list()
for thing in things:
    response = ddb_event_table.scan(FilterExpression=Attr('device_id').eq(thing['id']))
    events_count = len(response['Items'])
    if len(response['Items']) > 0:
        for event in response['Items']:
            event_data = dict()
            event_data['id'] = event['id']
            event_data['timestamp'] = event['timestamp']
            event_data['device_id'] = event['device_id']
            event_data['image'] = event['image_id']

            event_data['creatureweight'] = str(event['creature_weight'])
            event_data['foodlevel'] = str(event['food_level'])
            event_data['waterlevel'] = str(event['water_level'])

            events.append(event_data)

with open("s3/sightings.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "sightings.tmpl",
                                     {"events": events,
                                      "isadmin": isAdmin,
                                      "apiurl": api_url,
                                      "icon_path": "Things",
                                      "username": owner})
    html_file.write(file_content)


# Login page
with open("s3/login.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "login.tmpl",
                                      {"icon_path": "Things"})
    html_file.write(file_content)


# Login Success page
with open("s3/loginsuccess.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "loginsuccess.tmpl",
                                      {"icon_path": "Things",
                                       "username": owner})
    html_file.write(file_content)


# New Password page
with open("s3/loginnewpassword.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "loginnewpassword.tmpl",
                                      {"icon_path": "Things"})
    html_file.write(file_content)

# Password reset page
with open("s3/loginpasswordreset.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "loginpasswordreset.tmpl",
                                      {"icon_path": "Things"})
    html_file.write(file_content)

# Myhome reset page
with open("s3/myhome.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "myhome.tmpl",
                                      {"icon_path": "Things",
                                       "isadmin": isAdmin,
                                       "username": owner,
                                       "sightingscount": events_count,
                                       "mythingwarning":True})
    html_file.write(file_content)


# Settings page
with open("s3/settings.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "settings.tmpl",
                                      {"icon_path": "Things",
                                       "isadmin": isAdmin,
                                       "username": owner,
                                       "current_email_address": email_address})
    html_file.write(file_content)
