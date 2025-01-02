import json
import logging
import boto3
from update_task import update_task, TaskNotFoundError

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

    # パスパラメータから task_id を取得
    path_parameters = event.get("pathParameters")
    if not path_parameters or "taskId" not in path_parameters:
      error_message = "TaskID is missing in the path parameters"
      logger.warning(error_message)
      return error_handler(400, error_message)

    task_id = path_parameters["taskId"]
    logger.debug(f"Task ID: {task_id}")

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
      logger.error(f"Failed to decode: {str(e)}")
      return error_handler(400, "Request body is not valid JSON")

    task = update_task(table, task_id, task_data, user_id)

    # 成功レスポンスを返す
    return {
      "statusCode": 200,
      "body": json.dumps({
        "tasks": task
      })
    }

  except TaskNotFoundError as e:
    error_message = f"Task with ID '{task_id}' not found."
    logger.info(error_message)
    return error_handler(404, error_message)
    
  except Exception as e:
    logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
    return error_handler(500, "An unexpected error occurred")

def error_handler(statusCode: int, message: str):
  return {
        "statusCode": statusCode,
        "body": json.dumps({
            "error": message
        })
    }