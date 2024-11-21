import json
import os
import re

import vertexai
from geopy.distance import geodesic
from google.oauth2 import service_account
from template import PERSONA_TEMPLATE
from vertexai.generative_models import GenerativeModel
from boto3.dynamodb.types import TypeDeserializer


GEMINI_MODEL = os.environ["GEMINI_MODEL"]
DYNAMODB_PERSONA_TABLE = os.environ["DYNAMODB_PERSONA_TABLE"]
DYNAMODB_SATELLITEDATA_TABLE = os.environ["DYNAMODB_SATELLITEDATA_TABLE"]


TEST_SURROUNDING_INFO = [
    {
        "shop_lat": {"N": "37.39124887111705"},
        "shop_lng": {"N": "136.90151661513806"},
        "shop_name": {"S": "ファミリーマート 輪島中央店"},
        "shop_open_time": {"S": "7:30"},
        "shop_close_time": {"S": "18:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "コンビニエンスストア"},
    },
    {
        "shop_lat": {"N": "37.38744274629935"},
        "shop_lng": {"N": "136.90183371260338"},
        "shop_name": {"S": "クスリのアオキ 輪島店"},
        "shop_open_time": {"S": "11:00"},
        "shop_close_time": {"S": "20:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "ドラックストアで、日用品や食料品も売っている"},
    },
    {
        "shop_lat": {"N": "37.38635159313893"},
        "shop_lng": {"N": "136.90179079726164"},
        "shop_name": {"S": "ファッションセンターしまむら 輪島店"},
        "shop_open_time": {"S": "10:00"},
        "shop_close_time": {"S": "19:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "洋服店"},
    },
    {
        "shop_lat": {"N": "37.38652208686701"},
        "shop_lng": {"N": "136.90282076546356"},
        "shop_name": {"S": "ヤマダデンキ テックランド輪島店"},
        "shop_open_time": {"S": "10:00"},
        "shop_close_time": {"S": "17:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "家電量販店"},
    },
    {
        "shop_lat": {"N": "37.38707059062232"},
        "shop_lng": {"N": "136.90471856249755"},
        "shop_name": {"S": "ヤスサキ グルメ館 輪島店"},
        "shop_open_time": {"S": "9:00"},
        "shop_close_time": {"S": "19:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "食料品店"},
    },
    {
        "shop_lat": {"N": "37.39040306361326"},
        "shop_lng": {"N": "136.9067508475095"},
        "shop_name": {"S": "わじまおみやげ館"},
        "shop_open_time": {"S": "10:00"},
        "shop_close_time": {"S": "18:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "お土産屋"},
    },
    {
        "shop_lat": {"N": "37.39416967661686"},
        "shop_lng": {"N": "136.89729936172853"},
        "shop_name": {"S": "酒ブティックおくだ"},
        "shop_open_time": {"S": "10:00"},
        "shop_close_time": {"S": "18:00"},
        "is_24_hour": {"BOOL": False},
        "shop_description": {"S": "酒屋"},
    },
]

TEST_PERSONAS = [
    {
        "house_location": {
            "M": {"lat": {"N": "37.3984395"}, "lng": {"N": "136.8987622"}}
        },
        "age": {"N": "42"},
        "gender": {"S": "男性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "2"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "システムエンジニア"},
        "annual_income": {"N": "7500000"},
        "hobby": {"S": "ゴルフ"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3872560"}, "lng": {"N": "136.8999633"}}
        },
        "age": {"N": "35"},
        "gender": {"S": "女性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "1"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "看護師"},
        "annual_income": {"N": "4800000"},
        "hobby": {"S": "ヨガ"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3873960"}, "lng": {"N": "136.9028172"}}
        },
        "age": {"N": "28"},
        "gender": {"S": "男性"},
        "family": {"M": {"spouse": {"BOOL": False}, "children": {"N": "0"}}},
        "has_car": {"BOOL": False},
        "job": {"S": "公務員"},
        "annual_income": {"N": "4200000"},
        "hobby": {"S": "釣り"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.4012490"}, "lng": {"N": "136.9006156"}}
        },
        "age": {"N": "52"},
        "gender": {"S": "男性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "3"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "医師"},
        "annual_income": {"N": "12000000"},
        "hobby": {"S": "テニス"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3937342"}, "lng": {"N": "136.9014595"}}
        },
        "age": {"N": "45"},
        "gender": {"S": "女性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "2"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "会社役員"},
        "annual_income": {"N": "8500000"},
        "hobby": {"S": "ガーデニング"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3946083"}, "lng": {"N": "136.9018299"}}
        },
        "age": {"N": "33"},
        "gender": {"S": "女性"},
        "family": {"M": {"spouse": {"BOOL": False}, "children": {"N": "0"}}},
        "has_car": {"BOOL": False},
        "job": {"S": "デザイナー"},
        "annual_income": {"N": "4500000"},
        "hobby": {"S": "写真"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.4013490"}, "lng": {"N": "136.9046588"}}
        },
        "age": {"N": "48"},
        "gender": {"S": "男性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "1"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "大学教授"},
        "annual_income": {"N": "9200000"},
        "hobby": {"S": "読書"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3922265"}, "lng": {"N": "136.9041895"}}
        },
        "age": {"N": "39"},
        "gender": {"S": "男性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "2"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "営業職"},
        "annual_income": {"N": "6300000"},
        "hobby": {"S": "サイクリング"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3945565"}, "lng": {"N": "136.9144290"}}
        },
        "age": {"N": "41"},
        "gender": {"S": "女性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "1"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "薬剤師"},
        "annual_income": {"N": "5800000"},
        "hobby": {"S": "料理"},
    },
    {
        "house_location": {
            "M": {"lat": {"N": "37.3949108"}, "lng": {"N": "136.9003880"}}
        },
        "age": {"N": "37"},
        "gender": {"S": "男性"},
        "family": {"M": {"spouse": {"BOOL": True}, "children": {"N": "2"}}},
        "has_car": {"BOOL": True},
        "job": {"S": "会社員"},
        "annual_income": {"N": "5500000"},
        "hobby": {"S": "キャンプ"},
    },
]

deserializer = TypeDeserializer()


def _geopy_distance(lat1, lng1, lat2, lng2):
    point1 = (lat1, lng1)
    point2 = (lat2, lng2)
    distance = geodesic(point1, point2).kilometers
    return round(distance, 3)


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


def fetch_personas():
    personas = []
    # TODO: DynamoDBからとってくる
    for p in TEST_PERSONAS:
        personas.append({k: deserializer.deserialize(v) for k, v in p.items()})
    return personas


def _fetch_surrounding_info():
    # TODO: DynamoDBからとってくる
    shops = []
    for s in TEST_SURROUNDING_INFO:
        shops.append({k: deserializer.deserialize(v) for k, v in s.items()})
    return shops


def _create_surronding_info_prompt(persona_lat: float, persona_lng: float, shops: list):
    prompt = "近くのお店の情報は以下の通りです。\n      --------\n"
    for shop in shops:
        prompt += f"      店名: {shop['shop_name']}\n"
        prompt += f"      説明: {shop['shop_description']}\n"
        prompt += (
            f"      営業時間: {shop['shop_open_time']}-{shop['shop_close_time']}\n"
        )
        prompt += f"      あなたの家からの距離: {_geopy_distance(shop['shop_lat'], shop['shop_lng'], persona_lat, persona_lng)} km\n"
        prompt += "      --------\n"
    return prompt


def setup_gemini():
    credentials_info = {
        "type": "service_account",
        "project_id": os.environ["GOOGLE_CLOUD_PROJECT"],
        "private_key_id": os.environ["GOOGLE_PRIVATE_KEY_ID"],
        "private_key": os.environ["GOOGLE_PRIVATE_KEY"].replace("\\n", "\n"),
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


def execute_simulation(
    model, something_new: str, lat: float, lng: float, personas: list
):
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
        shops = _fetch_surrounding_info()

        other_info = {
            "surrounding_info": _create_surronding_info_prompt(
                persona["house_location"]["lat"],
                persona["house_location"]["lng"],
                shops,
            )
        }

        # print(f"{persona=}")
        # print(f"{something_new_info=}")

        prompt = PERSONA_TEMPLATE.safe_substitute(
            _flatten_dict(persona) | something_new_info | other_info
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
        print("=" * 20)

    return results
