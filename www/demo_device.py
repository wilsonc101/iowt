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

device_id = "2c5b7596-cc75-4a2e-b42d-a75a64c85028"
#device_id = "123abc"
#device_id ="098xyz"

device_token = "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.oRIgJ4aprPbFCGjnsSfA_9NnD1yDE2LLmXJeh53ZsPAsyMuy2N8J_tnbF_-MIU-VbNpI0An1yAngZf-KDWAxLIB_ZD-8Ss0w.vw62TETlUhZXhOxIlopb9A.RNAbQan-56XuBewGobuI-7qImsThE9RkhnHWBvaO5uPALK_sruzIAitApcx-FfC4gUVjx21ju6A5ubGk41Bjzg.Fn7F4o3ulos0z41pVMCEBzO6FIqQm-kv3HXF5N7t87o"

headers = {'Content-Type': 'application/json',
           'Device-Token': device_token}


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


c = HTTPSConnection("api.iowt.robotika.co.uk")
c.request('POST', '/event/newevent', content_as_string, headers=headers)
res = c.getresponse()
data = res.read().decode('utf-8')

print(data)


