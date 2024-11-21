import string

PERSONA_TEMPLATE = string.Template(
    """\
あなたの役割:
    あなたは、与えられた情報の住民として振舞ってください。
    次の緯度経度に「${something_new}」ができた場合に、
    その緯度経度付近に住んでいる住民のお気持ちを、30文字から50文字程度で考えてください。
    市民の気持ちのメッセージと、実際に行く確率をスコアとして出力してください。

情報:
    あなたの家と、${something_new}までの距離:
        ${distance} km
    住民の情報:
        - 年齢: ${age} 歳
        - 性別: ${gender}
        - 配偶者: ${family__spouse}
        - 子供: ${family__children} 人
        - 車: ${has_car}
        - 仕事: ${job}
        - 年収: ${annual_income} 円
        - 趣味: ${hobby}
    ${surrounding_info}

制約:
    - JSON形式で出力してください
    - messageは30文字から50文字にしてください
    - scoreは0から10までで設定してください
    - scoreは0に近いほど${something_new}に行きたくなく、10に近いほど${something_new}に行きたいことを示します

出力フォーマット:
    {
        message: string,
        score: number
    }

出力例:
    - {"message": "車もないし、歩いて40分は流石に遠い", "score": 2}
    - {"message": "車で15分くらいなので週末には家族で行きたい", "score": 7}
"""
)
