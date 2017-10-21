import boto3
import uuid
import json
from jwcrypto import jwt, jwk

DDB_CLIENT = boto3.client('dynamodb')


ddb_table = "iowt-devices"


def create_new_device():
    id = str(uuid.uuid4())
    key = jwk.JWK(generate="oct", size=256)
    key_data = json.loads(key.export())['k']
    token = jwt.JWT(header={"alg": "A256KW", "enc": "A256CBC-HS512"},
                    claims={"device_id": id})
    token.make_encrypted_token(key)

    return id, key_data, token.serialize()



device_id, key, token = create_new_device()

db_item = dict()
db_item['id'] = {'S': device_id}
db_item['deviceLocation'] = {'S': "Not Set"}
db_item['deviceName'] = {'S': "Not Set"}
db_item['deviceKey'] = {'S': key}
db_item['deviceToken'] = {'S': token}
db_item['deviceStatus'] = {'S': "new"}
db_item['deviceOwner'] = {'S': "none"}

DDB_CLIENT.put_item(TableName=ddb_table,
                    Item=db_item)


