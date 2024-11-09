# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
from crhelper import CfnResource

helper = CfnResource()

cognito_idp = boto3.client('cognito-idp')

def find_os_client(cognito_response):
  for client in cognito_response['UserPoolClients']:
    if client['ClientName'].lower().startswith("amazonopensearchservice"):
        return client['ClientId']

@helper.create
@helper.update
def retrieve_cognito_client(event,context):
  response_data = {
        'ClientId': None,
        'ClientSecret': None
    }

  try:
    UserPoolId = event['ResourceProperties']['UserPoolId']
    cognito_response = cognito_idp.list_user_pool_clients(UserPoolId=UserPoolId)
    client_id = find_os_client(cognito_response)
    cognito_response = cognito_idp.describe_user_pool_client(UserPoolId=UserPoolId, ClientId=client_id)

    response_data = {'ClientId': client_id, 'ClientSecret': cognito_response['UserPoolClient']['ClientSecret']}
    helper.Data.update(response_data)

  except Exception as e:
      print(f'Error: {e}')

@helper.delete
def no_op(_, __):
    print("Delete custom resource")

def handler(event, context):
    helper(event, context)