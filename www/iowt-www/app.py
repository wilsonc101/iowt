import base64
import copy
import botocore
import boto3
from boto3.dynamodb.conditions import Key, Attr
import jinja2
import sys
import json
import os
import urllib
import ast
import bleach


from chalice import Chalice, Response
app = Chalice(app_name='iowt-www')

S3_CLIENT = boto3.client('s3', region_name="eu-west-1")
IDP_CLIENT = boto3.client('cognito-idp')
DDB_CLIENT = boto3.client('dynamodb')
DDB_RESOURCE = boto3.resource('dynamodb')


icon_path = "Things"
default_header = {'Content-Type': 'text/html; charset=UTF-8'}

def render_s3_template(client, bucket, template_name, content=None):
    # If no conent is supplied, set to empty dict
    if content is None:
        content = dict()

    file_object = client.get_object(Bucket=bucket, Key=template_name)
    file_content = file_object['Body'].read().decode('utf-8')
    rendered_html = jinja2.Environment().from_string(file_content).render(content)

    return(rendered_html)


def get_user_data(headers):
    token_validation_url = os.environ['loginurl']
    try:
        access_token = None
        if "cookie" in headers:
            if len(headers['cookie']) > 0:
                cookie_data = headers['cookie']
                for cookie in cookie_data.split("; "):
                    cookie_name = cookie.split("=")[0]
                    cookie_content = cookie.split("=")[1]
                    if cookie_name == "access":
                        access_token = cookie_content

        if access_token:
            data = {'access_token': access_token}

            req = urllib.request.Request(token_validation_url)
            req.add_header('Content-Type', 'application/json')
            encoded_data = json.dumps(data).encode("utf-8")
            response = urllib.request.urlopen(req, encoded_data)
            response_data = response.read().decode("utf-8")

            response_json = json.loads(response_data)
            response_json['token'] = access_token

            if response_json['valid'] == "True":
                user_data = response_json
            else:
                user_data = False

        else:
            user_data = False

        return user_data

    except:
        return False


def trigger_admin_action(headers, action, actiondata="nothing"):
    # actions should expect JSON response
    admin_action_url = os.environ['adminactionurl']
    try:
        access_token = None
        if "cookie" in headers:
            if len(headers['cookie']) > 0:
                cookie_data = headers['cookie']
                for cookie in cookie_data.split("; "):
                    cookie_name = cookie.split("=")[0]
                    cookie_content = cookie.split("=")[1]
                    if cookie_name == "access":
                        access_token = cookie_content

        if access_token:
            data = {'access_token': access_token,
                    'action': action,
                    'action_data': actiondata}

            req = urllib.request.Request(admin_action_url)
            req.add_header('Content-Type', 'application/json')
            encoded_data = json.dumps(data).encode("utf-8")
            response = urllib.request.urlopen(req, encoded_data)
            response_data = response.read().decode("utf-8")

            response_json = json.loads(response_data)
            return response_json

        else:
            return False

    except:
        return str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])


def trigger_user_action(headers, action, actiondata=None):
    # actions should require username only (e.g password reset)
    user_action_url = os.environ['useractionurl']
    try:
        access_token = None
        if "cookie" in headers:
            if len(headers['cookie']) > 0:
                cookie_data = headers['cookie']
                for cookie in cookie_data.split("; "):
                    cookie_name = cookie.split("=")[0]
                    cookie_content = cookie.split("=")[1]
                    if cookie_name == "access":
                        access_token = cookie_content

        if access_token:
            data = {'access_token': access_token,
                    'action': action}

            req = urllib.request.Request(user_action_url)
            req.add_header('Content-Type', 'application/json')
            encoded_data = json.dumps(data).encode("utf-8")
            response = urllib.request.urlopen(req, encoded_data)
            response_data = response.read().decode("utf-8")

            return response_data

        else:
            return False

    except:
        return str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])


def check_device_token(device_id, token):
    device_auth_url = os.environ['deviceauthurl']
    try:
        data = {'Device-Id': device_id,
                'Device-Token': token}

        req = urllib.request.Request(device_auth_url)
        req.add_header('Content-Type', 'application/json')
        encoded_data = json.dumps(data).encode("utf-8")
        response = urllib.request.urlopen(req, encoded_data)
        response_data = response.read().decode("utf-8")

        response_json = json.loads(response_data)
        return response_json

    except:
        return {"result":"False", "data":str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])}


def update_device(table_name, device_id, device_location=None, device_name=None, device_owner=None):
    ddb_table = DDB_RESOURCE.Table(table_name)

    if device_owner is not None:
        # Assume this is an admin update
        response = ddb_table.update_item(
        Key={'id': device_id},
        UpdateExpression="SET deviceOwner=:value1",
        ExpressionAttributeValues={
            ':value1': device_owner},
        ReturnValues="UPDATED_NEW")

        return True

    else:
        # Otherwise assume this is a user update
        response = ddb_table.update_item(
        Key={'id': device_id},
        UpdateExpression="SET deviceLocation=:value1, deviceName=:value2",
        ExpressionAttributeValues={
            ':value1': device_location,
            ':value2': device_name},
        ReturnValues="UPDATED_NEW")

        return True

def delete_sighting(sighting_id, bucket_name, table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)

    # Delete table item(s)
    results = S3_CLIENT.list_objects(Bucket=bucket_name, Prefix=sighting_id)
    if 'Contents' not in results:
        return str(results)
    for s3_object in results['Contents']:
        S3_CLIENT.delete_object(Bucket=bucket_name, Key=s3_object['Key'])

    # Delete S3 items
    response = ddb_table.delete_item(Key={'id': sighting_id})

    return True


def get_user_things(username, table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)
    response = ddb_table.scan(FilterExpression=Attr('deviceOwner').eq(username))

    things = list()
    for item in response['Items']:
        things.append(item)

    return things


def get_all_things(table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)
    response = ddb_table.scan()

    things = list()
    for item in response['Items']:
        # Trim long entries
        if "deviceKey" in item:
            item['deviceKey'] = item['deviceKey'][:8] + "..."

        if "deviceToken" in item:
            item['deviceToken'] = "..." + item['deviceToken'][-8:]

        things.append(item)

    return things


def get_user_sightings(username, things, table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)
    events = list()

    for thing in things:
        response = ddb_table.scan(FilterExpression=Attr('device_id').eq(thing['id']))
        events_count = len(response['Items'])

        if events_count > 0:
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

    return events


def set_device_status(device_id, status, table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)

    response = ddb_table.update_item(
    Key={'id': device_id},
    UpdateExpression="SET deviceStatus=:value1",
    ExpressionAttributeValues={
        ':value1': status},
    ReturnValues="UPDATED_NEW")

    return True

def delete_device(device_id, table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)

    return True

def rekey_device(device_id, table_name):
    ddb_table = DDB_RESOURCE.Table(table_name)

    return True


## HTTP RETURNS
def _send_200(html_content):
    return Response(body=html_content,
                    status_code=200,
                    headers=default_header)

def _send_404():
    return Response(body="Not seen one of those before, best call Chris Packham!",
                    status_code=404,
                    headers=default_header)

def _send_500(content):
    return Response(body=content,
                    status_code=500,
                    headers=default_header)

def _send_login():
    s3_bucket = os.environ['bucket']
    html_content = render_s3_template(S3_CLIENT, s3_bucket,
                                              "login.tmpl",
                                              {"icon_path":icon_path})
    return _send_200(html_content)


@app.route('/',
           methods=['GET'])
def index():
    s3_bucket = os.environ['bucket']
    iowt_device_table = os.environ['iowt_device_table']
    iowt_events_table = os.environ['iowt_events_table']

    try:
        user_data = get_user_data(app.current_request.headers)

        # Reject request if no user data avaliable
        if not user_data:
            return _send_login()

        content = dict()
        content['username'] = user_data['username']
        content['isadmin'] = user_data['is_admin']
        content['icon_path'] = icon_path

        things = get_user_things(user_data['username'], iowt_device_table)

        mythingwarning = False
        for thing in things:
            if thing['deviceStatus'] != "online":
                mythingwarning = True

        content['mythingwarning'] = mythingwarning

        sightings = get_user_sightings(user_data['username'], things, iowt_events_table)
        content['sightingscount'] = len(sightings)


        html_content = render_s3_template(S3_CLIENT, s3_bucket,
                                          "myhome.tmpl", content)

        return _send_200(html_content)

    except:
        return _send_500(str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]))


@app.route('/{pages}',
           methods=['GET', 'POST'])
def showpage(pages):
    s3_bucket = os.environ['bucket']
    s3_event_bucket = os.environ['event_bucket']
    iowt_device_table = os.environ['iowt_device_table']
    iowt_events_table = os.environ['iowt_events_table']
    iowt_api_url = os.environ['iowt_api']
    sightings_image_url = os.environ['sightings_image_url']

    try:
        user_data = get_user_data(app.current_request.headers)

        # Reject request if no user data avaliable
        if not user_data:
            return _send_login()

        request = app.current_request
        # POST - Take incoming posted data (e.g. from forms)
        if request.method == 'POST':
            avaliable_pages = {"thingsadmin": "thingsadmin.tmpl",
                               "peopleadmin": "peopleadmin.tmpl",
                               "mythings": "mythings.tmpl",
                               "settings": "settings.tmpl",
                               "sightings": "sightings.tmpl"}

            # Reject unknown page
            if pages not in avaliable_pages:
                return _send_404()

            # mythings
            if pages == "mythings":
                post_data = ast.literal_eval(app.current_request.raw_body.decode('utf-8'))
                things = get_user_things(user_data['username'], iowt_device_table)

                for thing in things:
                    if thing['id'] == post_data['device-id']:
                        resp = update_device(device_id=post_data['device-id'],
                                             device_location=bleach.clean(post_data['device-location']),
                                             device_name=bleach.clean(post_data['device-name']),
                                             table_name=iowt_device_table)

                        return _send_200(resp)

                return send_404()

            # sightings
            elif pages == "sightings":
                post_data = ast.literal_eval(app.current_request.raw_body.decode('utf-8'))

                things = get_user_things(user_data['username'], iowt_device_table)
                sightings = get_user_sightings(user_data['username'], things, iowt_events_table)

                for sighting in sightings:
                    if sighting['id'] == post_data['eventid']:
                        resp = delete_sighting(sighting_id = post_data['eventid'],
                                               bucket_name = s3_event_bucket,
                                               table_name = iowt_events_table)

                        return _send_200(resp)

                return send_404()

            # thingsadmin
            elif pages == "thingsadmin":
                # Reject non-admin user
                if user_data['is_admin'] != "True":
                    return _send_404()

                post_data = ast.literal_eval(app.current_request.raw_body.decode('utf-8'))
                action = post_data['action']

                if action == "update":
                    resp = update_device(device_id=post_data['device-id'],
                                         device_owner=bleach.clean(post_data['device-owner']),
                                         table_name=iowt_device_table)

                    return _send_200(resp)

                elif action == "disable":
                    result = set_device_status(post_data['device-id'], "disabled", iowt_device_table)
                    return _send_200(result)

                elif action == "enable":
                    result = set_device_status(post_data['device-id'], "enabled", iowt_device_table)
                    return _send_200(result)

                elif action == "delete":
                    # Delete device and all related sightings
                    result = delete_device(post_data['device-id'], iowt_device_table)
                    return _send_200(result)

                elif action == "rekey":
                    # Regenerate token and key
                    pass

            # peopleadmin
            elif pages == "peopleadmin":
                # Reject non-admin user
                if user_data['is_admin'] != "True":
                    return _send_404()
                headers = app.current_request.headers

                post_data = ast.literal_eval(app.current_request.raw_body.decode('utf-8'))
                action = post_data['action']
                action_data = post_data['username']

                result = trigger_admin_action(headers, action, action_data)
                return _send_200(result)

            # settings
            elif pages == "settings":
                headers = app.current_request.headers

                post_data = ast.literal_eval(app.current_request.raw_body.decode('utf-8'))
                action = post_data['action']
                username = post_data['username']

                if action == "resetpassword":
                    result = trigger_user_action(headers, action)
                    return _send_200(result)

                # TODO: set attributes (i.e. email)


        # GET - Render page as requested
        elif request.method == "GET":
            avaliable_pages = {"thingsadmin": "thingsadmin.tmpl",
                               "peopleadmin": "peopleadmin.tmpl",
                               "myhome": "myhome.tmpl",
                               "mythings": "mythings.tmpl",
                               "settings": "settings.tmpl",
                               "sightings": "sightings.tmpl"}

            # Reject unknown page
            if pages not in avaliable_pages:
                return _send_404()

            # mythings
            if pages == "mythings":
                things = get_user_things(user_data['username'], iowt_device_table)

                content = dict()
                content['devices'] = things
                content['isadmin'] = user_data['is_admin']
                content['apiurl'] = iowt_api_url + "/" + pages
                content['icon_path'] = icon_path
                content['username'] = user_data['username']


            # sightings
            elif pages == "sightings":
                things = get_user_things(user_data['username'], iowt_device_table)
                sightings = get_user_sightings(user_data['username'], things, iowt_events_table)

                content = dict()
                content['icon_path'] = icon_path
                content['apiurl'] = iowt_api_url + "/" + pages
                content['isadmin'] = user_data['is_admin']
                content['username'] = user_data['username']
                content['events'] = sightings
                content['imageurl'] = sightings_image_url


            # thingsadmin
            elif pages == "thingsadmin":
                # Reject non-admin user
                if user_data['is_admin'] != "True":
                    return _send_404()

                things = get_all_things(iowt_device_table)

                content = dict()
                content['icon_path'] = icon_path
                content['apiurl'] = iowt_api_url + "/" + pages
                content['isadmin'] = user_data['is_admin']
                content['username'] = user_data['username']
                content['devices'] = things


            # peopleadmin
            elif pages == "peopleadmin":
                headers = app.current_request.headers

                # Reject non-admin user
                if user_data['is_admin'] != "True":
                    return _send_404()


                authapi_response = trigger_admin_action(headers, "getallusers")
                if not authapi_response:
                    return _send_500(authapi_response)

                else:
                    people = list()
                    content = dict()

                    for person in authapi_response:
                        people.append(authapi_response[person])

                    content['icon_path'] = icon_path
                    content['apiurl'] = iowt_api_url + "/" + pages
                    content['isadmin'] = user_data['is_admin']
                    content['username'] = user_data['username']
                    content['people'] = people

            # myhome
            elif pages == "myhome":
                content = dict()
                content['username'] = user_data['username']
                content['isadmin'] = user_data['is_admin']
                content['icon_path'] = icon_path

                things = get_user_things(user_data['username'], iowt_device_table)
                mythingwarning = False

                for thing in things:
                    if thing['deviceStatus'] != "online":
                        mythingwarning = True

                content['mythingwarning'] = mythingwarning

                sightings = get_user_sightings(user_data['username'], things, iowt_events_table)
                content['sightingscount'] = len(sightings)


            # settings
            elif pages == "settings":
                content = dict()
                content['icon_path'] = icon_path
                content['apiurl'] = iowt_api_url + "/" + pages
                content['isadmin'] = user_data['is_admin']
                content['username'] = user_data['username']
                content['current_email_address'] = user_data['email']

            html_content = render_s3_template(S3_CLIENT, s3_bucket,
                                                  avaliable_pages[pages],
                                                  content)

            return _send_200(html_content)


        # Reject unknown method (not that it should get here)
        else:
            return _send_404()

    except:
        return _send_500(str(sys.exc_info()) + " -- " + str(sys.exc_info()[1]))


@app.route('/image/{imageid}',
           methods=['GET'])
def makeimage(imageid):
    s3_event_bucket = os.environ['event_bucket']
    s3_bucket = os.environ['bucket']
    iowt_device_table = os.environ['iowt_device_table']

    try:
        user_data = get_user_data(app.current_request.headers)

        # Reject request if no user data avaliable
        if not user_data:
            return _send_login()

        # Get ids of 'things' owned by user
        things = get_user_things(user_data['username'], iowt_device_table)
        thing_ids = list()

        for thing in things:
            thing_ids.append(thing['id'])

        # Get image, return 404 if not found
        try:
            image_object = S3_CLIENT.get_object(Bucket=s3_event_bucket, Key=imageid)
        except S3_CLIENT.exceptions.NoSuchKey as e:
            return _send_404()

        image_metadata = image_object['Metadata']

        # Check device is owned by user
        if image_metadata['device_id'] in thing_ids:
            image_content = base64.b64encode(image_object['Body'].read())
            image = image_content.decode('utf-8')
            src_html = "data:image/png;base64,%s" % image

            return _send_200(src_html)

        else:
            return _send_404()

    except:
        return _send_500(str(sys.exc_info()) + " -- " + str(sys.exc_info()[1]))


@app.route('/newevent',
           methods=['POST'])
def event_post():
# Posted data structure
#HEADERS = {"Device-Token": JWE}
#CONTENT_TEMPLATE = {"timestamp": str(),
#                    "event_id": str(),
#                    "device_id": str()
#                    "event_data": {"creature_weight": int(),
#                                   "food_level": int(),
#                                   "water_level": int(),
#                                   "image_data": str(),
#                                   "image_type": str()}}

    try:
        headers = app.current_request.headers
        if 'Device-Token' not in headers:
            return _send_404()

        s3_bucket = os.environ['event_bucket']
        ddb_table = os.environ['iowt_events_table']

        request = app.current_request
        json_data = json.loads(request.raw_body.decode())


        token = headers['Device-Token']
        device_id = json_data['device_id']

        check_result = check_device_token(device_id, token)
        if not check_result['result']:
            return _send_404()


        file_content = base64.b64decode(json_data['event_data']['image_data'])
        metadata = {'timestamp': json_data['timestamp'],
                    'device_id': device_id}

        db_item = dict()
        db_item['id'] = {'S': json_data['event_id'] }
        db_item['timestamp'] = {'S': json_data['timestamp']}
        db_item['device_id'] = {'S': device_id}
        db_item['image_id'] = {'S': json_data['event_id'] + "." + json_data['event_data']['image_type']}
        db_item['creature_weight'] = {'N': str(json_data['event_data']['creature_weight'])}
        db_item['food_level'] = {'N': str(json_data['event_data']['food_level'])}
        db_item['water_level'] = {'N': str(json_data['event_data']['water_level'])}

        DDB_CLIENT.put_item(TableName=ddb_table,
                            Item=db_item)

        S3_CLIENT.put_object(Body=file_content,
                             Metadata=metadata,
                             Bucket=s3_bucket,
                             Key=json_data['event_id'] + "." + json_data['event_data']['image_type'])

        return _send_200("OK")

    except:
        return _send_500(str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]))



