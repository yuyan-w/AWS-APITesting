import logging

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def list_tasks(task_table, user_id: str):

  logger.info("Starting to fetch tasks from DynamoDB")

  try:
    # DynamoDBのqueryメソッドを使用して特定のuser_idのタスクを取得
    response = task_table.query(
        KeyConditionExpression="userId = :userId",
        ExpressionAttributeValues={
            ":userId": user_id  # パーティションキーに指定
        }
    )
    tasks = response.get("Items", [])
    logger.debug("Success to get Tasks list: {tasks}")

    return tasks

  except Exception as e:
    error_message = f"Failed to fetch tasks from DynamoDB: {str(e)}"
    logger.error(error_message, exc_info=True)
    raise RuntimeError(error_message)