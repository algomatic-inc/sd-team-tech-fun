import json
import os
import re

import boto3
import vertexai
from boto3.dynamodb.types import TypeDeserializer
from geopy.distance import geodesic
from google.oauth2 import service_account
from template import PERSONA_TEMPLATE, SATELLITE_INFO_TEMPLATE
from vertexai.generative_models import GenerativeModel

dynamo_client = boto3.client("dynamodb")

GEMINI_MODEL = os.environ["GEMINI_MODEL"]
DYNAMODB_PERSONA_TABLE = os.environ["DYNAMODB_PERSONA_TABLE"]
DYNAMODB_SATELLITE_DATA_TABLE = os.environ["DYNAMODB_SATELLITEDATA_TABLE"]


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

SATELLITE_INFO_LNG = [
    "136.876863425926",
    "136.88160416666673",
    "136.88634490740748",
    "136.89108564814822",
    "136.89582638888896",
    "136.9005671296297",
    "136.90530787037042",
    "136.91004861111116",
    "136.9147893518519",
    "136.91953009259265",
    "136.9242708333334",
    "136.92901157407414",
]

SATELLITE_INFO_LAT = [
    "37.37269675925923",
    "37.37743749999997",
    "37.382178240740714",
    "37.38691898148145",
    "37.391659722222194",
    "37.39640046296293",
    "37.40114120370367",
    "37.40588194444442",
    "37.41062268518515",
    "37.4153634259259",
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
    personal_ids = [str(i + 1) for i in range(10)]
    personas = []
    for personal_id in personal_ids:
        res = dynamo_client.get_item(
            TableName=DYNAMODB_PERSONA_TABLE, Key={"personaId": {"S": personal_id}}
        )
        personas.append(
            {k: deserializer.deserialize(v) for k, v in res["Item"].items()}
        )
    return personas


def _fetch_surrounding_info():
    # TODO: DynamoDBからとってくる
    shops = []
    for s in TEST_SURROUNDING_INFO:
        shops.append({k: deserializer.deserialize(v) for k, v in s.items()})
    return shops


def _get_satellite_key(lat, lng):
    # TODO: データが増えてきたら、2分探索とか
    # 入力を浮動小数点数に変換
    lat = float(lat)
    lng = float(lng)

    # 入力された経度以下の最大値を探す
    max_lng = max([l for l in SATELLITE_INFO_LNG if float(l) <= lng])
    # 入力された緯度以上の最大値を探す
    max_lat = min([l for l in SATELLITE_INFO_LAT if float(l) >= lat])

    # それぞれの値のインデックスを取得
    j = SATELLITE_INFO_LNG.index(max_lng)
    i = SATELLITE_INFO_LAT.index(max_lat)

    return f"{SATELLITE_INFO_LAT[i]}_{SATELLITE_INFO_LNG[j]}"


def _fetch_satellite_info(lat, lng) -> str:
    location_id = _get_satellite_key(lat, lng)

    res = dynamo_client.get_item(
        TableName=DYNAMODB_SATELLITE_DATA_TABLE,
        Key={"locationId": {"S": location_id}, "category": {"S": "sample"}},
    )
    res = {k: deserializer.deserialize(v) for k, v in res["Item"].items()}
    return SATELLITE_INFO_TEMPLATE.safe_substitute(res)


def _create_surrounding_info_prompt(
    persona_lat: float, persona_lng: float, shops: list
):
    prompt = ""
    for shop in shops:
        prompt += f"        店名: {shop['shop_name']}\n"
        prompt += f"        説明: {shop['shop_description']}\n"
        prompt += (
            f"        営業時間: {shop['shop_open_time']}-{shop['shop_close_time']}\n"
        )
        prompt += f"        あなたの家からの距離: {_geopy_distance(shop['shop_lat'], shop['shop_lng'], persona_lat, persona_lng)} km\n"
        prompt += "        --------\n"
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

        sattelite_info_arround_shomething_new = _fetch_satellite_info(lat, lng)
        shops = _fetch_surrounding_info()
        other_info = {
            "surrounding_info": _create_surrounding_info_prompt(
                persona["house_location"]["lat"],
                persona["house_location"]["lng"],
                shops,
            ),
            "sattelite_info_arround_shomething_new": sattelite_info_arround_shomething_new,
        }

        # print(f"{persona=}")
        # print(f"{something_new_info=}")

        prompt = PERSONA_TEMPLATE.safe_substitute(
            _flatten_dict(persona) | something_new_info | other_info
        )

        print(f"{prompt=}")

        # TODO: Quotaに引っかかってレスポンス取れないことがあるため暫定対応
        try:
            response = _get_gemini_response(model, prompt)
            if response is None:
                continue
        except Exception as e:
            print(f"{e=}")
            continue

        results.append(response | persona)
        print("=" * 20)

    return results
