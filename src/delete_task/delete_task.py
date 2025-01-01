import logging
from typing import Dict, Any

class TaskNotFoundError(Exception):
    """カスタム例外: タスクが見つからない場合"""
    pass

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def delete_task(task_table, task_id: str) ->  Dict[str, Any]:
  logger.info("Starting to delete task")

  # DynamoDBで更新処理を実行
  try:
    response = task_table.delete_item(
        Key={"taskId": task_id},
        ReturnValues="ALL_OLD"
      )
    deleted_task = response.get("Attributes", {})

    # deleted_task が存在しない場合は TaskNotFoundError を投げる
    if not deleted_task:
      error_message = f"Task with ID '{task_id}' not found."
      logger.debug(error_message)
      raise TaskNotFoundError(error_message)

    logger.info(f"Success to delete task: {deleted_task}")
    return deleted_task

  except TaskNotFoundError as e:
    raise
  
  except Exception as e:
    error_message = f"Failed to delete task with ID {task_id}: {str(e)}"
    logger.error(error_message, exc_info=True)
    raise RuntimeError(error_message)