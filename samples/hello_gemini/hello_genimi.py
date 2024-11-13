import argparse

import vertexai
from google.oauth2 import service_account
from vertexai.generative_models import GenerativeModel


def setup_gemini():
    # 認証情報を読み込む
    credentials = service_account.Credentials.from_service_account_file(
        "../../credentials/tf-satellite-hackathon-826dd6f95aca.json"
    )

    # Vertex AIの初期化（プロジェクトIDとロケーションを指定）
    vertexai.init(
        credentials=credentials,
        project="tf-satellite-hackathon",  # JSONファイルのproject_idを使用
        location="us-central1",  # Geminiが利用可能なリージョンを指定
    )

    # Geminiモデルのインスタンス作成
    return GenerativeModel("gemini-1.5-flash")


def get_gemini_response(model, prompt):
    # Geminiに質問を投げて回答を取得
    response = model.generate_content(
        prompt,
        generation_config={"max_output_tokens": 2048, "temperature": 0.9, "top_p": 1},
    )
    return response.text


def main():
    parser = argparse.ArgumentParser(description="Geminiに質問を投げるプログラム")
    parser.add_argument("prompt", type=str, help="Geminiへの質問内容")
    args = parser.parse_args()

    try:
        # Geminiのセットアップ
        model = setup_gemini()

        # 回答の取得と表示
        response = get_gemini_response(model, args.prompt)
        print("\nGeminiの回答:")
        print(response)

    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")


if __name__ == "__main__":
    main()
