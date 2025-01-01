import uuid
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from datetime import datetime

# ロガーの設定
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def create_task(task_table, task_data: Dict[str, Any], user_id: str) -> Dict[str, Any]:

  logger.info("Starting to create task")

  # 日本時間（UTC+9）を取得
  jst = timezone(timedelta(hours=9))
  current_time = datetime.now(jst).isoformat()

  # 必須フィールドチェック
  required_fields = ["title"]
  missing_fields = [field for field in required_fields if field not in task_data]
  if missing_fields:
      error_message = f"Missing required fields: {', '.join(missing_fields)}"
      logger.warning(error_message)
      raise ValueError(error_message)

  # タスクIDを生成
  task_id = str(uuid.uuid4())

  # タスクを作成
  task_item = {
    "taskId": task_id,
    "userId": user_id,
    "title": task_data["title"],
    "taskStatus": "NotStarted",
    "createdAt": current_time,
    "updatedAt": current_time
  }

  # タスクをDBに保存
  try:
    task_table.put_item(Item=task_item)
    logger.info(f"Success to save task to DynamoDB. Task ID: {task_id}")
  except Exception as e:
    error_message = f"Failed to save task to DynamoDB: {str(e)}"
    logger.error(error_message, exec_info=True)
    raise RuntimeError(error_message)

  return task_item
