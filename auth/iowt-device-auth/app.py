import sys
import boto3
import json
import os
import ast
from jwcrypto import jwt, jwk
from boto3.dynamodb.conditions import Key, Attr
from chalice import Chalice, Response

DDB_RESOURCE = boto3.resource('dynamodb')

app = Chalice(app_name='iowt-device-auth')

default_header = {'Content-Type': 'text/html; charset=UTF-8'}


def authenticate_device(device_id, token, table_name):
    try:
        ddb_table = DDB_RESOURCE.Table(table_name)

        key_type = "oct"
        key_template = {"k":None,
                        "kty": key_type}

        response = ddb_table.scan(FilterExpression=Attr('id').eq(device_id))

        # Should only return one item, anything else is wrong
        if len(response['Items']) != 1:
            return (False, {"result": "db lookup returned bad result count"})

        device_record = response['Items'][0]
        device_key = device_record['deviceKey']

        key = key_template
        key['k'] = device_key

        # Use key to decrypt token claims
        try:
            key = jwt.JWK(**key)
            ET = jwt.JWT(key=key, jwt=token).token
            claims = json.loads(ET.payload.decode('utf-8'))
        except:
            return (False, {"result": "decrypt failed -- " + str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])})

        # Check there is a device-id claim in the token
        if 'device_id' not in claims:
            return (False, {"result": "no id claims"})

        # Check claimed id matches one given in header
        if claims['device_id'] == device_id:
            return (True, {"result": "matching ids"})
        else:
            return (False, {"result": "no matching ids"})

    except:
        return (False, {"result": str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])})


## HTTP RETURNS
def _send_200(html_content):
    return Response(body=html_content,
                    status_code=200,
                    headers=default_header)

def _send_data_200(json_data):
    header = {'Content-Type': 'application/json; charset=UTF-8'}

    return Response(body=json_data,
                    status_code=200,
                    headers=header)

def _send_404():
    return Response(body="Not seen one of those before, best call Chris Packham!",
                    status_code=404,
                    headers=default_header)

def _send_500(content):
    return Response(body=content,
                    status_code=500,
                    headers=default_header)


@app.route('/deviceauth',
           methods=['POST'])
def index():
    iowt_device_table = os.environ['iowt_device_table']

    try:
        json_body = ast.literal_eval(app.current_request.raw_body.decode('utf-8'))

        if "Device-Id" not in json_body or "Device-Token" not in json_body:
            return _send_404()

        device_id = json_body['Device-Id'].decode("utf-8")
        device_token = json_body['Device-Token'].decode("utf-8")

        result, data = authenticate_device(device_id=device_id,
                                           token=device_token,
                                           table_name=iowt_device_table)

        return _send_data_200({"result":result, "data":data})


    except:
        return _send_500(str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]))

