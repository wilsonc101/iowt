import boto3
from boto3.dynamodb.conditions import Key, Attr
import base64

DDB_RESOURCE = boto3.resource('dynamodb')
S3_CLIENT = boto3.client('s3', region_name="eu-west-1")

ddb_device_table_name = "iowt-devices"
ddb_event_table_name = "iowt-events"
ddb_device_table = DDB_RESOURCE.Table(ddb_device_table_name)
ddb_event_table = DDB_RESOURCE.Table(ddb_event_table_name)

s3_event_bucket = "iowt-events"

owner = "chrisw"

image_id = "b7df85b5-1fa6-443b-bf2c-d89db07c5cf7.jpg"


# Loop through devices and pick all tagged with 'owner'
things = dict()
response = ddb_device_table.scan(FilterExpression=Attr('deviceOwner').eq(owner))
for item in response['Items']:
    things[item['id']] = item

image_name = image_id
image_object = S3_CLIENT.get_object(Bucket=s3_event_bucket, Key=image_name)
image_metadata = image_object['Metadata']

if image_metadata['device_id'] in things:
    print("this is yours")
else:
    print("nope")


#image_content = base64.b64encode(image_object['Body'].read())
#image = image_content.decode('utf-8')



#        with open(event['id'] + ".html", "w") as f:
#             f.write("<html><body>")
#             f.write('<img alt="Embedded Image" src="data:image/png;base64,%s"/>' % image)
#             f.write("</html></body>")

