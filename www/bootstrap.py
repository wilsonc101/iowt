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

isAdmin = True


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
                                       "isadmin": isAdmin})
    html_file.write(file_content)


# Loop through devices and pick all tagged with 'owner'
things = list()
response = ddb_device_table.scan(FilterExpression=Attr('owner').eq(owner))
for item in response['Items']:
    things.append(item)

with open("s3/mythings.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket,
                                      "mythings.tmpl",
                                      {"devices": things,
                                       "isadmin": isAdmin})
    html_file.write(file_content)


events = list()
# loop devices and get events
for thing in things:
    response = ddb_event_table.scan(FilterExpression=Attr('device_id').eq(thing['id']))
    if len(response['Items']) > 0:
        for event in response['Items']:
            event_data = dict()
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
                                      "isadmin": isAdmin})
    html_file.write(file_content)