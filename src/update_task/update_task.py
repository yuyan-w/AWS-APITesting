import logging
from typing import Dict, Any
from enum import Enum
from datetime import datetime, timedelta, timezone

class TaskNotFoundError(Exception):
    """カスタム例外: タスクが見つからない場合"""
    pass

class TaskStatus(Enum):
  NOT_STARTED = "NotStarted"
  IN_PROGRESS = "InProgress"
  COMPLETED = "Completed"

  @staticmethod
  def from_value(value: str):
    try:
      return TaskStatus(value)
    except ValueError:
      return TaskStatus.NOT_STARTED


# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def update_task(task_table, task_id: str, task_data:  Dict[str, Any], user_id: str) ->  Dict[str, Any]:
  logger.info("Starting to update task")

  # 日本時間（UTC+9）を取得
  jst = timezone(timedelta(hours=9))
  current_time = datetime.now(jst).isoformat()

  # 更新フィールドを動的に生成
  update_expression = []
  expression_values = {}

  # title または taskStatus のいずれかが存在することを確認
  if "title" not in task_data and "taskStatus" not in task_data:
    error_message = "At least one of 'title' or 'taskStatus' must be provided in the task data"
    logger.error(error_message)
    raise ValueError(error_message)

  # title が存在する場合
  if "title" in task_data:
    update_expression.append("title = :title")
    expression_values[":title"] = task_data["title"]

  # taskStatus が存在する場合
  if "taskStatus" in task_data:
    taskStatus = TaskStatus.from_value(task_data["taskStatus"])
    update_expression.append("taskStatus = :taskStatus")
    expression_values[":taskStatus"] = taskStatus.value

  # updatedAtを追加
  current_time = datetime.now(timezone.utc).isoformat()
  update_expression.append("updatedAt = :updatedAt")
  expression_values[":updatedAt"] = current_time
  
  update_expression_str = "SET " + ", ".join(update_expression)
  logger.debug(f"Update expression: {update_expression_str}")
  logger.debug(f"Expression attribute values: {expression_values}")

  # DynamoDBで更新処理を実行
  try:
    response = task_table.update_item(
        Key={
          "taskId": task_id,
          "userId": user_id
        },
        UpdateExpression=update_expression_str,
        ExpressionAttributeValues=expression_values,
        ReturnValues="ALL_NEW"
      )
    updated_task = response.get("Attributes", {})

    # updated_task が存在しない場合は TaskNotFoundError を投げる
    if not updated_task:
      error_message = f"Task with ID '{task_id}' not found."
      logger.debug(error_message)
      raise TaskNotFoundError(error_message)

    logger.info(f"Success to update task: {updated_task}")
    return updated_task
  
  except TaskNotFoundError as e:
    raise

  except Exception as e:
    error_message = f"Failed to update task with ID {task_id}: {str(e)}"
    logger.error(error_message, exc_info=True)
    raise RuntimeError(error_message)