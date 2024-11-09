# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
from crhelper import CfnResource

helper = CfnResource()
client_cognito_idp = boto3.client('cognito-idp')

@helper.create
@helper.update
def update_cognito_url_handler(event,context):
    user_pool_id = event['ResourceProperties']['UserPoolId']
    client_id = event['ResourceProperties']['ClientId']
    cloud_front_domain_name = event['ResourceProperties']['CloudFrontDistributionUrl']
    proxy_public_dns_name = event['ResourceProperties']['EC2ProxyPublicDnsName']

    try:
        response = client_cognito_idp.update_user_pool_client(
            UserPoolId=user_pool_id, 
            ClientId=client_id,
            CallbackURLs=[
                'https://'+cloud_front_domain_name+'/parseauth',
                'https://'+proxy_public_dns_name+'/_dashboards/app/home'
            ],
            LogoutURLs=[
                'https://'+cloud_front_domain_name+'/',
                'https://'+proxy_public_dns_name+'/_dashboards/app/home'
            ],
            SupportedIdentityProviders=[
                'COGNITO'
            ],
            AllowedOAuthFlows=[
                'code'
            ],
            AllowedOAuthScopes=[
                'openid',
                'email',
                'profile',
                'phone'
            ],
            AllowedOAuthFlowsUserPoolClient=True
            )
    except Exception as e:
        print(f'Error: {e}')

@helper.delete
def no_op(_, __):
    print("Delete custom resource")

def handler(event, context):
    print(event)
    helper(event, context)
