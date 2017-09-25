import json
import base64
import datetime
import uuid
import copy
from http.client import HTTPSConnection, HTTPConnection


CONTENT_TEMPLATE = {"timestamp": str(),
                    "event_id": str(),
                    "device_id": str(),
                    "event_data": {"creature_weight": int(),
                                   "food_level": int(),
                                   "water_level": int(),
                                   "image_data": str(),
                                   "image_type": str()}}


with open("img.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())

timestamp = datetime.datetime.strftime(datetime.datetime.now(), "%d/%m/%y %H:%M:%S")
event_id = str(uuid.uuid4())
creature_weight = 100
food_level = 100
water_level = 100
device_id = "123abc"

content = copy.deepcopy(CONTENT_TEMPLATE)
content["timestamp"] = timestamp
content["event_id"] = event_id
content["device_id"] = device_id
content["event_data"]["creature_weight"] = creature_weight
content["event_data"]["food_level"] = food_level
content["event_data"]["water_level"] = water_level
content["event_data"]["image_data"] = encoded_string.decode('utf-8')
content["event_data"]["image_type"] = "jpg"

content_as_string = json.dumps(content)

headers = {'Content-Type': 'application/json'}

c = HTTPSConnection("api.iowt.robotika.co.uk")
c.request('POST', '/event/newevent', content_as_string, headers=headers)
res = c.getresponse()
data = res.read()

print(data)


