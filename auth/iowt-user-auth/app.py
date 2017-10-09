import urlparse
import sys
import boto3
import botocore
import jwt
import datetime
import json
import jinja2
import os

from base64 import urlsafe_b64decode, b64decode
from Crypto.Util.number import bytes_to_long
from Crypto.PublicKey import RSA

from chalice import Chalice, Response
app = Chalice(app_name='iowt_auth')

from jwt.contrib.algorithms.pycrypto import RSAAlgorithm
#jwt.register_algorithm('RS256', RSAAlgorithm(RSAAlgorithm.SHA256))

idp_client = boto3.client('cognito-idp')
cognito_pool_id = os.environ['cogpoolid']
cognito_app_id = os.environ['cogappid']
cognito_admin_group = os.environ['cogadmgrp']
cognito_attribute = os.environ['cogattrib']

s3_client = boto3.client('s3', region_name="eu-west-1")
s3_bucket = os.environ['s3bucket']
pub_bucket_url = os.environ['pubbucketurl']

icon_path = os.environ['logopath']

tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime("%a, %d %b %Y %H:%M:%S GMT")
yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime("%a, %d %b %Y %H:%M:%S GMT")
default_header = {'Content-Type': 'text/html',
                  'Cache-Control': 'no-cache'}
default_css = pub_bucket_url + "style.css"
base_domain = os.environ['domain']

jwk_sets = {"keys":[{"alg":"RS256",
                     "e":"AQAB",
                     "kid":"H32BY5PfWdHIK3oUhnVzUX+witv8wajhnmDZJ1owCfw=",
                     "kty":"RSA",
                     "n":"hZFDtkImBWD78i4lUTsJNxNibrOSpgpTu_RSMqv2eUavJ9sk-ZuZ4HndvMKnKjRRbTXT9575F45DdQPWHUC0U3-1B3cnV7K6VkY1TbSqucFiGPI9ByePt0w1O8oqajxjRk-Mgj-LYfvmKzzcY5jG-LLcnc6zbBRj5241DgushFzHinSmD9sGV5-agsfpU3aVJdAfFn0GeopghLxj8fbxGDJCLFRbPrrtsuHc_aproNH9HtzBd5P9FxpQ-AHIHnBTv124DtOdxvWYpESSzJontJY-D5McRqs_DOsgHz8bb74773QWTU7ToLoQ6MpOgw-VFWYWw5VkqWK_tLCcGOPCew",
                     "use":"sig"},
                    {"alg":"RS256",
                     "e":"AQAB",
                     "kid":"IbTvN43O0tvA171V///Rh+N5aBKJu1fRHaoHpUMJxyk=",
                     "kty":"RSA",
                     "n":"qvlQb4H_r3BdTL-VH9VuN0QwOPU6TdvqDJP6aQwl1o0wE5zpNBS5ANMfHs6cg8OVduoC_jU98sZs5WfCdUcbUFwzTNGcHIrkmFx97IgnwQz5QhKf_NG4SWDE7dMu0O0208jH6cr6qMkoyCKYxkMbbSUbzFOXnoevxoSslskUG_4guG5w_z1PzKn9bk9b_l9GgrZ_xBn8rkiLEIdRk2nteKNwcuajOM4KvCKCvSTitlw5Zru6Lt_RqUDbLwAKJ8fIZIWbjtHQFOIRaQUQNwxY5KCluvLJZMSeA9mixC-C3aUMbFpPxNtyol4RMUvTtTzNZtcdMdE_7AqBNMW9cz6LrQ",
                     "use":"sig"}]}

auth_parameters_template = {"UserPoolId": None,
                           "ClientId": None,
                           "AuthParameters": {"USERNAME": None,
                                              "PASSWORD": None}}

def _base64_pad(s):
    return (s + '=' * (4 - len(s) % 4))


def get_token_data(jwk_sets, token):
    header, payload, signature = str(token).split(".")
    try:
        # Get token segements and elements
        header_str = urlsafe_b64decode(_base64_pad(header))
        header_json = json.loads(header_str, 'utf-8')

        kid = header_json['kid']
        alg = header_json['alg']

        # Find matching kid and algorithm, then verify
        for jwks in jwk_sets['keys']:
            if (jwks['kid'] == kid and jwks['alg'] == alg):
                e_b64 = _base64_pad(jwks['e'])
                n_b64 = _base64_pad(jwks['n'])
                e_bytes = urlsafe_b64decode(e_b64)
                n_bytes = urlsafe_b64decode(n_b64)

                modulus = bytes_to_long(e_bytes)
                exponant = bytes_to_long(n_bytes)

                public_key = RSA.construct((exponant, modulus))
                public_key_pem = public_key.publickey().exportKey()


        token_data = jwt.decode(token, key=public_key_pem, algorithms=[alg])
        return(True, token_data)

    except:
        return(False, str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]))


def set_new_password(client, session_id,
                     auth_parameters, new_password,
                     challenge_name="NEW_PASSWORD_REQUIRED"):

    response = client.admin_respond_to_auth_challenge(ChallengeName=challenge_name,
                                                      ClientId=auth_parameters['ClientId'],
                                                      UserPoolId=auth_parameters['UserPoolId'],
                                                      Session=session_id,
                                                      ChallengeResponses={'NEW_PASSWORD': new_password,
                                                                          'USERNAME': auth_parameters['AuthParameters']['USERNAME']})

    return response


def reset_password(client, cognito_app_id,
                   username, verification_code, new_password):

    try:
        response = client.confirm_forgot_password(ClientId=cognito_app_id,
                                                  Username=username,
                                                  ConfirmationCode=verification_code,
                                                  Password=new_password)
        return response

    except:
        return False


def do_login(client, auth_parameters, auth_flow="ADMIN_NO_SRP_AUTH"):

    try:
        response = client.admin_initiate_auth(AuthFlow=auth_flow,
                                              ClientId=auth_parameters['ClientId'],
                                              UserPoolId=auth_parameters['UserPoolId'],
                                              AuthParameters=auth_parameters['AuthParameters'])
        return(True, response)


    except botocore.exceptions.ClientError as e:
        error_code =  e.response['Error']['Code']

        if error_code == "PasswordResetRequiredException":
            # Login was accepted but a new password is required
            return(True, {"ChallengeName": "PASSWORD_RESET_REQUIRED"})

        else:
            # Login seems to have been accepted but returned an unknown code
            return(False, str(sys.exc_info()[1]))

    except:
        return(False, str(sys.exc_info()[1]))


def _get_user_attributes(client, userpool_id, username):
    try:
        response = client.admin_get_user(Username=username,
                                         UserPoolId=userpool_id)

        return(True, response['UserAttributes'])

    except:
        return(False, str(sys.exc_info()[1]))


def set_user_attribute(client, userpool_id, username, attrib_name, attrib_value):
    try:
        response = client.admin_update_user_attributes(Username=username,
                                                       UserPoolId=userpool_id,
                                                       UserAttributes=[{'Name': attrib_name,
                                                                        'Value': attrib_value}])
        return(True, None)

    except:
        return(False, str(sys.exc_info()[1]))


def has_attribute(client, userpool_id, username, attribute="email"):
    result, data = _get_user_attributes(client, userpool_id, username)

    if result:
        for item in data:
            if item['Name'] == attribute:
                return(True, item['Value'])

        return(False, None)

    else:
        return(result, data)


def _get_user_groups(client, userpool_id, username):
    try:
        response = client.admin_list_groups_for_user(Username=username,
                                                     UserPoolId=userpool_id)

        return(True, response['Groups'])

    except:
        return(False, sys.exc_info()[1])


def is_admin(client, userpool_id, username, admin_group="admin"):
    result, data = _get_user_groups(client, userpool_id, username)

    if result:
        admin_user = False
        for group in data:
            if group['GroupName'] == admin_group:
                admin_user = True

        return(result, admin_user)

    else:
        return(result, data)


def render_s3_template(client, bucket, template_name, content=None):
    # If no conent is supplied, set to empty dict
    if content is None:
        content = dict()

    file_object = client.get_object(Bucket=bucket, Key=template_name)
    file_content = file_object['Body'].read() .decode('utf-8')
    rendered_html = jinja2.Environment().from_string(file_content).render(content)
#    client.put_object(Bucket=bucket, Key="test_file1.txt", Body=rendered_html)

    return(str(rendered_html))


@app.route('/authform')
def auth_form():
    try:
        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        {"csspath": default_css})
        return Response(body=login_form,
                        status_code=200,
                        headers=default_header)

    except:
        return Response(body=str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]),
                        status_code=500,
                        headers=default_header)


@app.route('/authin',
           methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def auth_in():
    try:
        parsed = urlparse.parse_qs(app.current_request.raw_body)
        username = parsed['username'][0]
        password = parsed['password'][0]

        auth_params = auth_parameters_template
        auth_params['UserPoolId'] = cognito_pool_id
        auth_params['ClientId'] = cognito_app_id
        auth_params['AuthParameters']['USERNAME'] = username
        auth_params['AuthParameters']['PASSWORD'] = password

        content = {"csspath": default_css,
                   "icon_path": icon_path,
                   "username":username}

        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        content)

        new_password_form = render_s3_template(s3_client,
                                               s3_bucket,
                                               "loginnewpassword.tmpl",
                                               content)

        reset_password_form = render_s3_template(s3_client,
                                                 s3_bucket,
                                                 "loginpasswordreset.tmpl",
                                                 content)

        login_success = render_s3_template(s3_client,
                                           s3_bucket,
                                           "loginsuccess.tmpl",
                                           content)

        parsed = urlparse.parse_qs(app.current_request.raw_body)
        username = parsed['username'][0]
        password = parsed['password'][0]

        auth_params = auth_parameters_template
        auth_params['UserPoolId'] = cognito_pool_id
        auth_params['ClientId'] = cognito_app_id
        auth_params['AuthParameters']['USERNAME'] = username
        auth_params['AuthParameters']['PASSWORD'] = password

        login_response = do_login(idp_client, auth_params)

        if login_response[0] is True:
            if "ChallengeName" not in login_response[1]:
                ## User account is functional - return tokens
                login_response = login_response[1]

                access_token = login_response['AuthenticationResult']['AccessToken']
                refresh_token = login_response['AuthenticationResult']['RefreshToken']
                id_token = login_response['AuthenticationResult']['IdToken']

                default_header['Access-Control-Allow-Origin'] = '*'
                default_header['Set-Cookie'] = 'username=' + username + ';' + \
                                               'Expires=' + tomorrow + ';' + \
                                               'Path=/;' + \
                                               'Domain=' + base_domain
                default_header['Set-cookie'] = 'access=' + access_token + ';' + \
                                               'Expires=' + tomorrow + ';' + \
                                               'Path=/;' + \
                                               'Domain=' + base_domain


                return Response(body=login_success,
                       status_code=200,
                       headers=default_header)

            else:
                ## Authentication returned a challenge
                if login_response[1]['ChallengeName'] == "NEW_PASSWORD_REQUIRED":
                # New required (because a temporary password is set)
                    session_id = login_response[1]['Session']

                    default_header['Access-Control-Allow-Origin'] = '*'
                    default_header['Set-Cookie'] = 'username=' + username + ';' + \
                                                   'Expires=' + tomorrow + ';' + \
                                                   'Path=/;' + \
                                                   'Domain=' + base_domain
                    default_header['Set-cookie'] = 'session=' + session_id + ';' + \
                                                   'Expires=' + tomorrow + ';' + \
                                                   'Path=/;' + \
                                                   'Domain=' + base_domain

                    return Response(body=new_password_form,
                           status_code=200,
                           headers=default_header)

                elif login_response[1]['ChallengeName'] == "PASSWORD_RESET_REQUIRED":
                # Password reset required - no session cookie present
                    default_header['Access-Control-Allow-Origin'] = '*'
                    default_header['Set-Cookie'] = 'username=' + username + ';' + \
                                                   'Expires=' + tomorrow + ';' + \
                                                   'Path=/;' + \
                                                   'Domain=' + base_domain

                    return Response(body=reset_password_form,
                                    status_code=200,
                                    headers=default_header)

        else:
            content['error_message'] = "Sorry, something went wrong. Please try again<br><br>" + str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]) + "<br><hr>" + str(login_response)

            default_header['Access-Control-Allow-Origin'] = '*'
            default_header['Set-Cookie'] = 'access="";'

            login_form = render_s3_template(s3_client,
                                            s3_bucket,
                                            "login.tmpl",
                                            content)

            return Response(body=login_form,
                            status_code=200,
                            headers=default_header)

    except:
        content['error_message'] = "Sorry, something went wrong. Please try again<br><br>" + str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])
        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        content)

        return Response(body=login_form,
                        status_code=500,
                        headers=default_header)


@app.route('/newpass', methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def auth_new_password():
    content = {"csspath": default_css,
               "icon_path": icon_path}
    try:
        # Extract cookie data
        cookie_data = app.current_request.headers['cookie']
        for cookie in cookie_data.split("; "):
            cookie_name = cookie.split("=")[0]
            cookie_content = cookie.split("=")[1]
            if cookie_name == "access":
                access_token = cookie_content
            elif cookie_name == "username":
                username = cookie_content
                content['username'] = username
            elif cookie_name == "session":
                session_id = cookie_content

        # Extract HTML form data
        parsed = urlparse.parse_qs(app.current_request.raw_body)
        password = parsed['password'][0]

        auth_params = auth_parameters_template
        auth_params['UserPoolId'] = cognito_pool_id
        auth_params['ClientId'] = cognito_app_id
        auth_params['AuthParameters']['USERNAME'] = username
        auth_params['AuthParameters']['PASSWORD'] = password

        response = set_new_password(idp_client, session_id, auth_params, password)
        if "ChallengeName" not in response:
            access_token = response['AuthenticationResult']['AccessToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']
            id_token = response['AuthenticationResult']['IdToken']

            login_success = render_s3_template(s3_client,
                                               s3_bucket,
                                               "loginsuccess.tmpl",
                                               content)

            default_header['Access-Control-Allow-Origin'] = '*'
            default_header['Set-Cookie'] = 'username=' + username + ';' + \
                                           'Expires=' + tomorrow + ';' + \
                                           'Path=/;' + \
                                           'Domain=' + base_domain
            default_header['Set-cookie'] = 'access=' + access_token + ';' + \
                                           'Expires=' + tomorrow + ';' + \
                                           'Path=/;' + \
                                           'Domain=' + base_domain
            default_header['set-cookie'] = 'session="";' + \
                                           'Path=/;' + \
                                           'Domain=' + base_domain

            return Response(body=login_success,
                   status_code=200,
                   headers=default_header)

        else:
            content['error_message'] = "Sorry, something went wrong. Please try again<br><br>" + str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]) + "<br><hr>" + str(login_response)
            login_form = render_s3_template(s3_client,
                                            s3_bucket,
                                            "login.tmpl",
                                            content)

            return Response(body=login_form,
                            status_code=200,
                            headers=default_header)

    except:
        content['error_message'] = "Sorry, something went wrong. Please try again<br><br>" + str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])
        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        content)

        return Response(body=login_form,
                        status_code=200,
                        headers=default_header)


@app.route('/resetpass',
           methods=['POST'],
           content_types=['application/x-www-form-urlencoded'])
def auth_reset_password():
    content = {"csspath": default_css,
               "icon_path": icon_path}
    try:
        # Extract cookie data
        cookie_data = app.current_request.headers['cookie']
        for cookie in cookie_data.split("; "):
            cookie_name = cookie.split("=")[0]
            cookie_content = cookie.split("=")[1]
            if cookie_name == "access":
                access_token = cookie_content
            elif cookie_name == "username":
                username = cookie_content
            elif cookie_name == "session":
                session_id = cookie_content

        # Extract HTML form data
        parsed = urlparse.parse_qs(app.current_request.raw_body)
        password = parsed['password'][0]
        verification_code = parsed['code'][0]


        response = reset_password(idp_client, cognito_app_id, username, verification_code, password)
        assert response, "error reseting password"

        content['error_message'] = "Your password has been reset."
        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        content)

        return Response(body=login_form,
                        status_code=200,
                        headers=default_header)

    except:
        content['error_message'] = "Sorry, something went wrong. Please try again<br><br>" + str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])
        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        content)

        return Response(body=login_form,
                        status_code=200,
                        headers=default_header)


@app.route('/read')
def read_cookie():
    content = {"csspath": default_css,
               "icon_path": icon_path}

    try:
        cookie_data = app.current_request.headers['cookie']
        for cookie in cookie_data.split("; "):
            cookie_name = cookie.split("=")[0]
            cookie_content = cookie.split("=")[1]
            if cookie_name == "access":
                access_token = cookie_content
            elif cookie_name == "username":
                username = cookie_content
            elif cookie_name == "session":
                session_id = cookie_content

        result, data = get_token_data(jwk_sets, str(access_token))

        if result:
            if 'username' in data:
                content['username'] = data['username']
                # Get admin group membership
                result, admin_user = is_admin(idp_client,
                                              cognito_pool_id,
                                              data['username'],
                                              admin_group=cognito_admin_group)
                if admin_user:
                    content['is_admin'] = "True"
                else:
                    content['is_admin'] = "False"

                # Get lemputer name
                attrib_name = "custom:" + cognito_attribute
                result, attrib_value = has_attribute(idp_client,
                                                     cognito_pool_id,
                                                     data['username'],
                                                     attribute=attrib_name)

                if attrib_value is not None:
                    content['identifier'] = attrib_value
                else:
                    content['identifier'] = "Not Set"

                html_content = render_s3_template(s3_client,
                                                  s3_bucket,
                                                  "userinfo.tmpl",
                                                  content)

        else:
            html_content = "Ooops, something went wrong!<br><br>" + str(result) + " -- " + str(data)

        return Response(body=html_content,
                        status_code=200,
                        headers=default_header)

    except:
        content['error_message'] = "Sorry, something went wrong. Please try again<br><br>" + \
                                   str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1])

        login_form = render_s3_template(s3_client,
                                        s3_bucket,
                                        "login.tmpl",
                                        content)

        return Response(body=login_form,
                        status_code=500,
                        headers=default_header)

@app.route('/clear')
def clear_cookie():
    try:
        default_header['Set-Cookie'] = 'username="";' + \
                                       'Expires=' + yesterday + ';' + \
                                       'Path=/;' + \
                                       'Domain=' + base_domain
        default_header['Set-cookie'] = 'access="";' + \
                                       'Expires=' + yesterday + ';' + \
                                       'Path=/;' + \
                                       'Domain=' + base_domain
        default_header['set-cookie'] = 'session="";' + \
                                       'Expires=' + yesterday + ';' + \
                                       'Path=/;' + \
                                       'Domain=' + base_domain

        return Response(body="clear",
                        status_code=200,
                        headers=default_header)

    except:
        return Response(body=str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]),
                        status_code=500,
                        headers=default_header)

@app.route('/validatetoken',
           methods=['POST'])
def validate_token():
    try:
        json_body = app.current_request.json_body
        access_token = json_body['access_token'].decode("utf-8")

        result, data = get_token_data(jwk_sets, access_token)

        response_data = {'valid': str(result)}

        if result:
            response_data['data'] = data

            if 'username' in data:
                response_data['username'] = data['username']
                # Get admin group membership
                result, admin_user = is_admin(idp_client,
                                              cognito_pool_id,
                                              data['username'],
                                              admin_group=cognito_admin_group)
                if admin_user:
                    response_data['is_admin'] = "True"
                else:
                    response_data['is_admin'] = "False"

                # Get identifier
                attrib_name = "custom:" + cognito_attribute
                result, attrib_value = has_attribute(idp_client,
                                                     cognito_pool_id,
                                                     data['username'],
                                                     attribute=attrib_name)

                if attrib_value is not None:
                    response_data['identifier'] = attrib_value
                else:
                    response_data['identifier'] = "Not Set"

        default_header['Content-Type'] = 'application/json; charset=UTF-8'

        return Response(body=json.dumps(response_data),
                        status_code=200,
                        headers=default_header)

    except:
        return Response(body=str(sys.exc_info()[0]) + " -- " + str(sys.exc_info()[1]),
                        status_code=500,
                        headers=default_header)


