import boto3
from boto3.dynamodb.conditions import Key, Attr
import jinja2


DDB_RESOURCE = boto3.resource('dynamodb')
S3_CLIENT = boto3.client('s3', region_name="eu-west-1")

ddb_device_table_name = "iowt-devices"
ddb_event_table_name = "iowt-events"
ddb_device_table = DDB_RESOURCE.Table(ddb_device_table_name)
ddb_event_table = DDB_RESOURCE.Table(ddb_event_table_name)

s3_bucket = "iowt"

owner = "chrisw"



def render_s3_template(client, bucket, template_name, content=None):
    # If no conent is supplied, set to empty dict
    if content is None:
        content = dict()

    file_object = client.get_object(Bucket=bucket, Key=template_name)
    file_content = file_object['Body'].read().decode('utf-8')
    rendered_html = jinja2.Environment().from_string(file_content).render(content)

    return(rendered_html)


# Loop through devices and pick all tagged with 'owner'
things = list()
response = ddb_device_table.scan(FilterExpression=Attr('owner').eq(owner))
for item in response['Items']:
    things.append(item)

# loop devices and get events
#for thing in things.keys():
#    response = ddb_event_table.scan(FilterExpression=Attr('device_id').eq(thing))
#    things[thing]['events'] = response['Items']

with open("../s3/device.html", "w") as html_file:
    file_content = render_s3_template(S3_CLIENT, s3_bucket, "mythings.tmpl", {"devices": things})
    html_file.write(file_content)
#                    <td>{{device.id}}</td>
#                    <td><em>{{device.name}}</em></td>
#                    <td><em>{{</em></td>
#                    device.status == "online" 

