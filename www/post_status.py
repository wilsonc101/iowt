import json
import base64
import datetime
import uuid
import copy
from http.client import HTTPSConnection, HTTPConnection


device_id = "2c5b7596-cc75-4a2e-b42d-a75a64c85028"
device_token = "eyJhbGciOiJBMjU2S1ciLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIn0.oRIgJ4aprPbFCGjnsSfA_9NnD1yDE2LLmXJeh53ZsPAsyMuy2N8J_tnbF_-MIU-VbNpI0An1yAngZf-KDWAxLIB_ZD-8Ss0w.vw62TETlUhZXhOxIlopb9A.RNAbQan-56XuBewGobuI-7qImsThE9RkhnHWBvaO5uPALK_sruzIAitApcx-FfC4gUVjx21ju6A5ubGk41Bjzg.Fn7F4o3ulos0z41pVMCEBzO6FIqQm-kv3HXF5N7t87o"

headers = {'Content-Type': 'application/json',
           'Device-Token': device_token}


c = HTTPSConnection("api.iowt.robotika.co.uk")
c.request('POST', '/check/status', json.dumps({"device_id": device_id}), headers=headers)
res = c.getresponse()
data = res.read().decode('utf-8')

print(str(res.status) + " -- " + data)


