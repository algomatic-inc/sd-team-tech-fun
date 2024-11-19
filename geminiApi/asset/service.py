import json
import os
import re

import vertexai
from geopy.distance import geodesic
from google.oauth2 import service_account
from template import PERSONA_TEMPLATE
from vertexai.generative_models import GenerativeModel

GEMINI_MODEL = os.environ["GEMINI_MODEL"]
DYNAMODB_PERSONA_TABLE = os.environ["DYNAMODB_PERSONA_TABLE"]
DYNAMODB_SATELLITEDATA_TABLE = os.environ["DYNAMODB_SATELLITEDATA_TABLE"]


TEST_PERSONAS = [
    {
        "house_location": {"lat": 35.681236, "lng": 139.767125},
        "age": 45,
        "gender": "男性",
        "family": {"spouse": True, "children": 2},
        "has_car": True,
        "job": "エンジニア",
        "annual_income": 8000000,
        "hobby": "釣り",
    },
    {
        "house_location": {"lat": 34.693738, "lng": 135.502165},
        "age": 32,
        "gender": "女性",
        "family": {"spouse": False, "children": 0},
        "has_car": False,
        "job": "グラフィックデザイナー",
        "annual_income": 6000000,
        "hobby": "ヨガ",
    },
    {
        "house_location": {"lat": 43.062095, "lng": 141.354376},
        "age": 29,
        "gender": "男性",
        "family": {"spouse": False, "children": 0},
        "has_car": True,
        "job": "教師",
        "annual_income": 4500000,
        "hobby": "写真撮影",
    },
]


def _geopy_distance(lat1, lng1, lat2, lng2):
    point1 = (lat1, lng1)
    point2 = (lat2, lng2)
    distance = geodesic(point1, point2).kilometers
    return distance


def _flatten_dict(nested_dict, parent_key="", sep="__"):
    flat_dict = {}

    for key, value in nested_dict.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if type(value) == bool:
            value = "あり" if value else "なし"
        if isinstance(value, dict):
            flat_dict.update(_flatten_dict(value, new_key, sep=sep))
        else:
            flat_dict[new_key] = value

    return flat_dict


def _extract_json(json_like_str) -> dict:
    # 正規表現で 'message' と 'score' が含まれるJSON部分を抽出
    pattern = r"\{.*?\"message\"\s*:\s*\".*?\",.*?\"score\"\s*:\s*\d+.*?\}"

    # 該当する部分を検索
    match = re.search(pattern, json_like_str, re.DOTALL)

    if match:
        # マッチしたJSON部分を取り出す
        json_str = match.group(0)
        try:
            # JSON文字列を辞書に変換
            json_data = json.loads(json_str)
            return json_data
        except json.JSONDecodeError:
            print("無効なJSON形式です")
    else:
        print("JSON部分が見つかりませんでした")

    return None


def get_personas():
    return TEST_PERSONAS


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

    return GenerativeModel(GEMINI_MODEL)


def _get_gemini_response(model, prompt: str) -> dict:

    response = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": 2048,
            "temperature": 0.9,
            "top_p": 1,
        },
    )
    print(f"{response.text=}")
    return _extract_json(response.text)


def execute_simulation(model, something_new: str, lat: str, lng: str, personas: list):
    results = []
    for persona in personas:
        something_new_info = {
            "something_new": something_new,
            "something_new__lat": lat,
            "something_new__lng": lng,
            "distance": _geopy_distance(
                lat,
                lng,
                float(persona["house_location"]["lat"]),
                float(persona["house_location"]["lng"]),
            ),
        }

        print(f"{persona=}")
        print(f"{something_new_info=}")

        prompt = PERSONA_TEMPLATE.safe_substitute(
            _flatten_dict(persona) | something_new_info
        )

        print(f"{prompt=}")

        response = _get_gemini_response(model, prompt)
        if response is None:
            continue
        results.append(
            response
            | {
                "house_location": {
                    "lat": persona["house_location"]["lat"],
                    "lng": persona["house_location"]["lng"],
                }
            }
        )

    return results
