import argparse
from pathlib import Path

import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel, Image, Part

PROJECT_ROOT_DIR = Path(__file__).parent.parent.parent
IMAGE_DIR = Path(__file__).parent / "output"


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


def main():
    # parser = argparse.ArgumentParser(description="Geminiに質問を投げるプログラム")
    # parser.add_argument("prompt", type=str, help="Geminiへの質問内容")
    # args = parser.parse_args()

    prompt = """以下がどのくらい存在していると想定されますか？
それぞれ、０から１０で推定し、以下のフォーマットで返却してください。
```
住宅地: [0-10]
公共施設: [0-10]
商業施設: [0-10]
工業施設: [0-10]
山林: [0-10]
"""
    image_path = IMAGE_DIR / "tile_136.9147893518519_37.391659722222194.png"

    try:
        # Geminiのセットアップ
        model = setup_gemini()

        # 回答の取得と表示
        response = get_gemini_response(model, prompt, image_path)
        print("\nGeminiの回答:")
        print(response)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
