import json
from decimal import Decimal
import traceback

from service import execute_simulation, get_personas, setup_gemini


def _decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def make_response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False, default=_decimal_default_proc),
    }


def lambda_handler(event, context):
    print(event)
    try:
        body = (
            json.loads(event["body"])
            if isinstance(event.get("body"), str)
            else event.get("body", {})
        )
        lat = body.get("lat")
        lng = body.get("lng")

        if lat is None or lng is None:
            return make_response(400, {"error": "location info (lat, lng) is required"})

        personas = get_personas()

        model = setup_gemini()

        res = execute_simulation(
            model,
            "AEONの新店舗",
            lat,
            lng,
            personas,
        )

        return make_response(200, res)

    except Exception as e:
        print(traceback.format_exc())
        return make_response(500, {"error": str(e)})
