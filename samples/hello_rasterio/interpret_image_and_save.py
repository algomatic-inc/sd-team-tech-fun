import re
from decimal import Decimal
from pathlib import Path
from typing import Dict

import boto3
import vertexai
import yaml
from boto3.dynamodb.types import TypeSerializer
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Image, Part

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent
IMAGE_DIR = Path(__file__).parent / "output"

session = boto3.Session(profile_name="knowledge")
client = session.client("dynamodb")
serializer = TypeSerializer()

pattern = re.compile(r"[A-z]*:\s\d")

# TODO: レスポンスに"```yaml"のようなMarkdownの形式を含んでしまうため、回避する必要がある。
PROMPT = """以下がどのくらい存在していると想定されますか？
それぞれの項目が占める割合を0から10の整数で推定してください。
出力は以下のフォーマットに従い、YAML形式の内容を出力してください。
ただし、コードブロックやMarkdownの形式は含めず、純粋なYAMLデータだけを提供してください。

出力例:
housing: 1
commercialFacilities: 2
industrialFacilities: 0
publicFacilities: 4
parkingLot: 5
road: 6
park: 7
waterArea: 8
agriculturalArea: 9
woodland: 10
"""


def setup_gemini():
    # 認証情報を読み込む
    credentials = service_account.Credentials.from_service_account_file(
        PROJECT_ROOT_DIR / "credentials/tf-satellite-hackathon-826dd6f95aca.json"
    )

    # Vertex AIの初期化（プロジェクトIDとロケーションを指定）
    vertexai.init(
        credentials=credentials,
        project="tf-satellite-hackathon",  # JSONファイルのproject_idを使用
        location="us-central1",  # Geminiが利用可能なリージョンを指定
    )

    # Geminiモデルのインスタンス作成
    return GenerativeModel("gemini-1.5-flash")


def get_gemini_response(model: GenerativeModel, prompt, image_path):
    # Geminiに質問を投げて回答を取得
    image = Part.from_image(image=Image.load_from_file(image_path))
    response = model.generate_content(
        [prompt, image],
        generation_config={"max_output_tokens": 2048, "temperature": 0.9, "top_p": 1},
    )
    return response.text


def get_lat_lng_from_filename(image_path: Path):
    # ファイル名から緯度経度を抽出するための関数
    # 例: "tile_136.9147893518519_37.391659722222194.png" -> (37.391659722222194, 136.9147893518519)
    parts = image_path.stem.split("_")
    if len(parts) >= 3:
        lat = Decimal(parts[-1])
        lon = Decimal(parts[-2])
        return (lat, lon)
    else:
        return None


def clean_response(response: str):
    # Geminiの回答から不要な部分を削除するための関数
    response = "\n".join([l for l in response.split("\n") if pattern.match(l)])

    return yaml.safe_load(response)


def save_to_dynamodb(lat: Decimal, lng: Decimal, response: Dict[str, int]):
    # DynamoDBに保存するための関数
    client.put_item(
        TableName="SatelliteData",
        Item={
            "locationId": {"S": f"{lat}_{lng}"},
            "category": {"S": "sample"},
            "lat": {"N": str(lat)},
            "lng": {"N": str(lng)},
            **{k: serializer.serialize(v) for k, v in response.items()},
        },
    )


def main():
    # parser = argparse.ArgumentParser(description="Geminiに質問を投げるプログラム")
    # parser.add_argument("prompt", type=str, help="Geminiへの質問内容")
    # args = parser.parse_args()

    image_path = IMAGE_DIR / "tile_136.9147893518519_37.391659722222194.png"
    lat, lng = get_lat_lng_from_filename(image_path)

    try:
        # Geminiのセットアップ
        model = setup_gemini()

        # 回答の取得と表示
        response = get_gemini_response(model, PROMPT, image_path)
        response = clean_response(response)
        print("\nGeminiの回答:")
        print(response)

        save_to_dynamodb(lat, lng, response)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
