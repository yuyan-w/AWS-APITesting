import json
import logging
import boto3
from create_task import create_task

# DynamoDBテーブルの初期化
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
  try:
    logger.debug("Received event: %s", json.dumps(event))

    # ユーザーIDの取得
    user_id = event['requestContext']['authorizer']['claims']['sub']
    logger.debug("User ID: %s", user_id)

    # リクエストボディの取得
    body = event.get("body")
    if body is None:
      error_message = "Request body is missing"
      logger.warning(error_message)
      return error_handler(400, error_message)
    
    # JSON形式に変換
    try:
      task_data = json.loads(body)
      logger.debug(f"Parsed task data: {task_data}")
    except json.JSONDecodeError as e:
      logger.error(f"Failed to decode JSON. Error: {str(e)}")
      return error_handler(400, "Request body is not valid JSON")
    
    # タスクを作成処理を実行
    task = create_task(table, task_data, user_id)
    logger.info(f"Success to create task. Task ID: {task["taskId"]}")

    # 成功レスポンスを返す
    return {
      "statusCode": 200,
      "body": json.dumps({
        "task": task
      })
    }
    
  except Exception as e:
    logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
    return error_handler(500, "An unexpected error occurred")

def error_handler(statusCode: int, message: str):
  logger.debug(f"StatusCode: {statusCode}, Message: {message}")
  return {
        "statusCode": statusCode,
        "body": json.dumps({
            "error": message
        })
    }