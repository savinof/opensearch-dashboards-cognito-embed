# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

def handler(event, context):
    # Get the response from the origin
    response = event['Records'][0]['cf']['response']

    # Modify Set-Cookie header if present
    if 'set-cookie' in response['headers']:

        filtered_set_cookie = []
        # Loop through each Set-Cookie header
        for cookie_header in response['headers']['set-cookie']:
            
            # filter out set-cookie headers containing ID-TOKEN, REFRESH-TOKEN, and ACCESS-TOKEN and append "; SameSite=Strict to the rest"
            if not any(key in cookie_header['value'] for key in ['ID-TOKEN', 'REFRESH-TOKEN', 'ACCESS-TOKEN']):
                filtered_set_cookie.append({'key': 'set-cookie', 'value': cookie_header['value'] + "; SameSite=Strict"})
            response['headers']['set-cookie'] = filtered_set_cookie

    # Return the modified response
    return response