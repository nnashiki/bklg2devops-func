import azure.functions as func
from backlog_schema import AddTaskRequest
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

import logging
import json
import os

logger = logging.getLogger(__name__)


def gen_tasks(devops_org, devops_pat, devops_project_id, backlog_org, backlog_project_key, backlog_task_id, task_title, task_desc):
    organization_url = f"https://dev.azure.com/{devops_org}"
    backlog_task_url = f"https://{backlog_org}.backlog.com/view/{backlog_project_key}-{backlog_task_id}"

    # Create a connection to the org
    credentials = BasicAuthentication("", devops_pat)
    connection = Connection(base_url=organization_url, creds=credentials)
    # クライアントの取得
    work_item_tracking_client = connection.clients.get_work_item_tracking_client()

    # ユーザーストーリーの作成
    create_user_story_command = [
        {"op": "add", "path": "/fields/System.Title", "from": None, "value": task_title},
        {"op": "add", "path": "/fields/System.Description", "from": None, "value": f"origin: {backlog_task_url} <br> {task_desc}"},
    ]
    created_user_story = work_item_tracking_client.create_work_item(
        create_user_story_command, devops_project_id, "User Story"
    )

    # タスクの作成
    create_task_command = [
        {"op": "add", "path": "/fields/System.Title", "from": None, "value": task_title},
        {"op": "add", "path": "/fields/System.Description", "from": None, "value": f"origin: {backlog_task_url} <br> {task_desc}"},
    ]
    created_task = work_item_tracking_client.create_work_item(create_task_command, devops_project_id, "Task")

    # ユーザーストーリとタスクの紐付け
    task_update_command = [
        {
            "op": "add",
            "path": "/relations/-",
            "value": {
                "rel": "System.LinkTypes.Hierarchy-Reverse",
                "url": f"https://dev.azure.com/{devops_project_id}/_apis/wit/workItems/{str(created_user_story.id)}",
            },
        }
    ]
    work_item_tracking_client.update_work_item(task_update_command, created_task.id, devops_project_id)


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    logger.debug(req_body)
    add_task_req = AddTaskRequest.parse_obj(req_body)
    logger.debug(add_task_req)

    gen_tasks(devops_org=os.environ['DEVOPS_ORG'],
              devops_pat=os.environ['DEVOPS_PAT'],
              devops_project_id=os.environ['DEVOPS_PROJECT_ID'],
              backlog_org=os.environ['BACKLOG_ORG'],
              backlog_project_key=add_task_req.project.projectKey,
              backlog_task_id=add_task_req.content.id,
              task_title=add_task_req.content.summary,
              task_desc=add_task_req.content.description)

    return func.HttpResponse(
        json.dumps({"result": "success"}),
        status_code=200,
        mimetype="application/json",
    )
