import boto3
import json

idp_client = boto3.client('cognito-idp')

cog_pool_id = ""

def get_all_users(client, userpool_id):
    try:
        response = client.list_users(UserPoolId=userpool_id)

        people = dict()
        for user in response['Users']:
            person = dict()
            person['personUsername'] = user['Username']

            if user['Enabled']:
                person['personStatus'] = "enabled"
            else:
                person['personStatus'] = "disabled"

            for attribute in user['Attributes']:
                if attribute['Name'] == "email":
                    person['personEmail'] = attribute['Value']
                elif attribute['Name'] == "email_verified":
                    person['personEmailVerified'] = attribute['Value']

            people[user['Username']] = person

        return(True, people)

    except:
        return(False, sys.exc_info()[1])



result, users = get_all_users(idp_client, cog_pool_id)

people = list()

for i in users:
    people.append(users[i])


print(people)


