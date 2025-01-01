import json

def lambda_handler(event, context):
    # トラブルシューティング用に event と context をログ出力
    print("Event: %s", json.dumps(event))
    print("Context: %s", context)

    # パスパラメータの取得
    path_parameters = event.get("pathParameters", {})
    task_id = path_parameters.get("taskId", None)  # /tasks/{taskId}

    # クエリパラメータの取得
    query_parameters = event.get("queryStringParameters", {}) or {}
    user_id = query_parameters.get("userId", None)  # ?userId=123

    # リクエストボディの取得
    body = event.get("body", "{}")
    try:
        body_data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        body_data = {"error": "Invalid JSON format"}

    # レスポンスの構築
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "SUCCESS",
            "taskId": task_id,
            "userId": user_id,
            "body": body_data
        })
    }

    return response
