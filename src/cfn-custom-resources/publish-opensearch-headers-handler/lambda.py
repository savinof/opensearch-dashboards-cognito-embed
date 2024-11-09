# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
from crhelper import CfnResource

helper = CfnResource()
lambda_client = boto3.client('lambda')

@helper.create
@helper.update
def publish_opensearch_headers_handler(event,context):
  function_name = event['ResourceProperties']['OpensearchHeadersHandler']

  try:
      publish_response = lambda_client.publish_version(FunctionName=function_name)
      function_arn = publish_response['FunctionArn']
      response_data = {'FunctionArn': function_arn}
      print(response_data)
      helper.Data.update(response_data)

  except Exception as e:
      print(f'Error: {e}')

@helper.delete
def no_op(_, __):
    print("Delete custom resource")

def handler(event, context):
    print(event)
    helper(event, context)
