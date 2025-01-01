import json

def lambda_handler(event, context):
    print("テスト用のLambda関数を実行 by SAM")
    print(f"Event: {event}")
    print(f"Context: {context}")
    
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello, World! by SAM"})
    }