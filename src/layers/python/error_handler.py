import json

def error_handler(statusCode: int, message: str):
    return {
            "statusCode": statusCode,
            "body": json.dumps({
                "error": message,
                "msg": "in layer"
            })
        }