import json

def lambda_handler(event, context):
    # API Gatewayから渡されたリクエスト情報をログに記録
    print(f"Received event: {json.dumps(event)}")

    # Cognito Authorizerのユーザー情報を取得
    user_info = event.get('requestContext', {}).get('authorizer', {})

    if user_info:
        print(f"User information from Cognito Authorizer: {json.dumps(user_info)}")
    else:
        print("No user information found in the authorizer context.")

    # レスポンスを返す
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'User information logged successfully.',
            'userInfo': user_info
        })
    }
