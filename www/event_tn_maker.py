from PIL import Image
from io import BytesIO
import boto3
from boto3.dynamodb.conditions import Key, Attr
import base64

DDB_RESOURCE = boto3.resource('dynamodb')
S3_CLIENT = boto3.client('s3', region_name="eu-west-1")

ddb_device_table_name = "iowt-devices"
ddb_event_table_name = "iowt-events"
ddb_device_table = DDB_RESOURCE.Table(ddb_device_table_name)
ddb_event_table = DDB_RESOURCE.Table(ddb_event_table_name)

s3_bucket = "iowt-events"

owner = "chrisw"
thumb_size = 128, 128


# Loop through devices and pick all tagged with 'owner'
things = dict()
response = ddb_device_table.scan(FilterExpression=Attr('owner').eq(owner))
for item in response['Items']:
    things[item['id']] = item


# loop devices and get events
for thing in things.keys():
    response = ddb_event_table.scan(FilterExpression=Attr('device_id').eq(thing))
    things[thing]['events'] = response['Items']


for i in things:
    for event in things[i]['events']:
        image_name = event['image_id']
        image_object = S3_CLIENT.get_object(Bucket=s3_bucket, Key=image_name)
        image_content = base64.b64encode(image_object['Body'].read())
        image = image_content.decode('utf-8')

        with open(event['id'] + ".html", "w") as f:
             f.write("<html><body>")
             f.write('<img alt="Embedded Image" src="data:image/png;base64,%s"/>' % image)
             f.write("</html></body>")

        im_buffer = BytesIO()
        im = Image.open(BytesIO(base64.b64decode(image)))
        im.thumbnail(thumb_size)
        im.save(im_buffer, format="JPEG")
        thumb_content = im_buffer.getvalue()

        S3_CLIENT.put_object(Body=thumb_content,
                             Bucket=s3_bucket,
                             Key=event['id'] + "_thumb.jpg")
