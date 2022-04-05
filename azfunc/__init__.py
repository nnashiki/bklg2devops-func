import azure.functions as func

import logging
import json

logger = logging.getLogger(__name__)


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body = req.get_json()
    logger.debug(req_body)

    if 'hoge' in req_body:
        result = req_body['hoge']
    else:
        result = "success"

    return func.HttpResponse(
        json.dumps({"result": result}),
        status_code=200,
        mimetype="application/json",
    )
