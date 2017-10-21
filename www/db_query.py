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


# Admin - Loop through devices
things = list()
response = ddb_device_table.scan()
for item in response['Items']:
    things.append(item)


# Loop through devices and pick all tagged with 'owner'
things = list()
response = ddb_device_table.scan(FilterExpression=Attr('owner').eq(owner))
for item in response['Items']:
    things.append(item)
 #   print(item)

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

#print(len(events))



sample_data = {'device-id': '123abc', 'device-name': 'Inside', 'device-location': 'Out the front', 'action': 'update'}


response = ddb_device_table.update_item(
    Key={
        'id': sample_data['device-id']
    },
    UpdateExpression="SET deviceLocation=:value1, deviceName=:value2",
    ExpressionAttributeValues={
        ':value1': sample_data['device-location'],
        ':value2': sample_data['device-name'],
    },
    ReturnValues="UPDATED_NEW"
)
