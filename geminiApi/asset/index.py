import json
import traceback

from service import execute_simulation, get_personas, setup_gemini


def make_response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body, ensure_ascii=False),
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

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"response": res}, ensure_ascii=False),
        }

    except Exception as e:
        print(traceback.format_exc())
        return make_response(500, {"error": str(e)})
