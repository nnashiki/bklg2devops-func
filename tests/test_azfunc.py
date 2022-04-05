import json
import azure.functions as func
from bklg2devops import main


class TestFunction:
    def test_first(self):
        json_str = """
{
  "id": 0,
  "project": {
    "id": 0,
    "projectKey": "project.projectKey",
    "name": "project.name",
    "chartEnabled": true,
    "subtaskingEnabled": false,
    "projectLeaderCanEditProjectLeader": false,
    "useWikiTreeView": true,
    "textFormattingRule": "markdown",
    "archived": false
  },
  "type": 1,
  "content": {
    "id": 100,
    "key_id": 100,
    "summary": "test issue",
    "description": "test description",
    "issueType": {
      "id": 100,
      "projectId": 100,
      "name": "test",
      "color": "#e30000",
      "displayOrder": -1
    },
    "resolution": null,
    "priority": {
      "id": 3,
      "name": "中"
    },
    "status": {
      "id": 1,
      "name": "未対応"
    },
    "assignee": null,
    "category": [],
    "versions": [],
    "milestone": [],
    "startDate": null,
    "dueDate": null,
    "estimatedHours": null,
    "actualHours": null,
    "parentIssueId": null,
    "customFields": [],
    "attachments": []
  },
  "notifications": [],
  "createdUser": {
    "id": 0,
    "userId": null,
    "name": "createdUser.name",
    "roleType": 2,
    "lang": "ja",
    "mailAddress": null,
    "nulabAccount": {
      "nulabId": "nulabAccount.nulabId",
      "name": "nulabAccount.name",
      "uniqueId": "nulabAccount.uniqueId"
    }
  },
  "created": "2022-04-01T09:00:00Z"
}
        """
        print(json.loads(json_str))
        req = func.HttpRequest(
            method="POST",
            body=json_str.encode(),
            url="/api/azfunc",
            headers={},
        )
        resp = main(req)
        assert resp.status_code == 200
        resp_json = json.loads(resp.get_body().decode())

