import json
import logging
import boto3
from list_tasks import list_tasks
from error_handler import error_handler

# DynamoDBテーブルの初期化
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('TasksTable')

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def lambda_handler(event, context):
  try:
    logger.debug("Received event: %s", json.dumps(event))

    # TODO: 削除
    # テスト用のエラーです
    # raise ValueError("This is TEST Error")

    # ユーザーIDの取得
    user_id = event['requestContext']['authorizer']['claims']['sub']
    logger.debug("User ID: %s", user_id)

    tasks = list_tasks(table, user_id)
    logger.info(f"Get Task List: {tasks}")

    # 成功レスポンスを返す
    return {
      "statusCode": 200,
      "body": json.dumps({
        "tasks": tasks
      })
    }
    
  except Exception as e:
    logger.error(f"Unexpected error occurred: {str(e)}", exc_info=True)
    return error_handler(500, "An unexpected error occurred")
