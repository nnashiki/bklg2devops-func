import json
import azure.functions as func
from azfunc import main


class TestFunction:
    def test_first(self):
        req = func.HttpRequest(
            method="POST",
            body=json.dumps(
                {"hoge": "foo"}
            ).encode("utf-8"),
            url="/api/azfunc",
            headers={},
        )
        resp = main(req)
        assert resp.status_code == 200
        resp_json = json.loads(resp.get_body().decode())
        assert resp_json["result"] == "foo"

    def test_second(self):
        req = func.HttpRequest(
            method="POST",
            body=json.dumps({}).encode("utf-8"),
            url="/api/azfunc",
            headers={},
        )
        resp = main(req)
        assert resp.status_code == 200
        resp_json = json.loads(resp.get_body().decode())
        assert resp_json["result"] == "success"
