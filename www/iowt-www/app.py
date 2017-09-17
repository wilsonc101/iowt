import botocore
import boto3
import jinja2
import sys
import json
import os

import urllib

from chalice import Chalice, Response
app = Chalice(app_name='iowt-www')


S3_CLIENT = boto3.client('s3', region_name="eu-west-1")
IDP_CLIENT = boto3.client('cognito-idp')

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


@app.route('/')
def index():
    s3_bucket = os.environ['bucket']
    pub_bucket_url = os.environ['pubbucketurl']
    default_css = pub_bucket_url + "style.css"


    try:
        user_data = get_user_data(app.current_request.headers)

        # Reject request if no user data avaliable
        if not user_data:
            return Response(body="Please login to access mapping",
                            status_code=200,
                            headers=default_header)

        content = dict()
        content['username'] = user_data['username']
        content['is_admin'] = user_data['is_admin']
        content['identifier'] = user_data['identifier']
        content['csspath'] = default_css

        html_content = render_s3_template(S3_CLIENT, s3_bucket, "demo.tmpl", content)

        return Response(body=html_content,
                        status_code=200,
                        headers={'Content-Type': 'text/html',
                                 'Access-Control-Allow-Origin': '*'})
    except:
        return Response(body=str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]),
                        status_code=500,
                        headers=default_header)

