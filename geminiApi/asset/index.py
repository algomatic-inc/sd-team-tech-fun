import json
import os

import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel


def setup_gemini():
    credentials_info = {
        "type": "service_account",
        "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
        "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
        "private_key": os.environ["GOOGLE_PRIVATE_KEY"],
        "client_email": os.environ["GOOGLE_CLIENT_EMAIL"],
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.environ["GOOGLE_CLIENT_X509_CERT_URL"],
        "universe_domain": "googleapis.com",
    }

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info
    )

    vertexai.init(
        credentials=credentials,
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("VERTEX_LOCATION", "us-central1"),
    )

    return GenerativeModel("gemini-1.5-flash")


def lambda_handler(event, context):
    print(event)
    try:
        body = (
            json.loads(event["body"])
            if isinstance(event.get("body"), str)
            else event.get("body", {})
        )
        prompt = body.get("prompt", "")

        if not prompt:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Prompt is required"}),
            }

        model = setup_gemini()
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 2048,
                "temperature": 0.9,
                "top_p": 1,
            },
        )

        print(response.text)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"response": response.text}, ensure_ascii=False),
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": str(e)}, ensure_ascii=False),
        }
