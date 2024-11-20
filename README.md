# Team Tech Fun
Satellite Data Days ~ 衛星画像ハッカソン ~

Team Tech Funの開発リポジトリです

### Demo URL
https://tf-satellite-hackathon-frontend.s3.ap-northeast-1.amazonaws.com/index.html

### イベントURL
https://lu.ma/vnnro5q4?tk=olCl0z

## 🤖 技術要素
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white&style=flat)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&style=flat)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white&style=flat)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-web-services&logoColor=white&style=flat)

## 📁 フォルダ構成
https://uithub.com/algomatic-inc/sd-team-tech-fun

## ⚙️ 環境構築
### WSL
| name | version |
| --- | --- |
| nvm | 0.39.7 |
| node | v20.11.0 |
| npm | 10.2.4 |
| pnpm | 9.9.0 |
| uv | 0.5.1 |
| aws | 2.15.17 |
| cdk | 2.167.0 |

#### uv
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
uv --version
# uv 0.5.1
```

あとは下記でよしなに

https://qiita.com/moritalous/items/569e0910413e0835520c

#### cdk
```bash
npm install -g aws-cdk
cdk --version
# 2.167.0 (build 677e108)
```

### 参考サイト・リンク
### 衛星画像データURL
https://drive.google.com/drive/folders/1719scq9f1g80v5Y7W3jXFWhUyR-RQRxb

### 株式会社Penetrator様ご提供 API README
https://algomatic.notion.site/Penetrator-README-9c47a07b5ef343268fda2351854ecf40

### GeoTiffをPythonで扱う方法について
https://drive.google.com/file/d/1DSUvACsZa4T_76hR9rTDnJ9vo_8lEZjf/view

## 👩‍🏫 テスト
Nothing to do

## ⚡️ デプロイ
### Frontend
```bash
cd frontend
pnpm run deploy
```

### Backend
```bash
cd geminiApi
cdk synth
cdk deploy
```

### Infra
```bash
cd infra
cdk synth
cdk deploy
```

対象のAWSアカウントは別途管理

## 🎯 機能
現在検討中...

## 💡 選択テーマ
​未来の都市と社会を創造するデジタルツール

## ⚠️ 制限事項/注意事項
- ご提供されているデータの取扱いに注意すること
- ご提供されているAPIの取扱いに注意すること

## ✅ TODO
(GitHub Project作れなかった...)
- [x] ~~技術検証~~
  - [x] ~~Gemini呼び出し~~
  - [x] ~~提供されたAPIの呼び出し~~
  - [x] ~~衛星画像データから都合の良いデータに変換する~~
    - 位置情報
    - 属性値
      - （例）光の度合いを見て、田舎か都会か判定する
  - [x] ~~上記のデータ作成に生成AIを活用できるか~~
  - [x] ~~ペルソナを持たせたAIの行動シミュレーション~~
    - ペルソナの持たせ方
    - ペルソナのパラメータ
      - 偏屈おじさんみたいのがいても良いかも
      - 超合理的な人
      - 超感情的な人
      - etc.,
    - 行動判定
  - [ ] （余力あれば）他の衛星データ（Tellus?）を利用してみる
  - [ ] （余力あれば）自治体データを利用してみる
- [ ] Frontend
  - [x] ~~Google Map APIから地図を取得する~~
  - [x] ~~取得した地図を表示する~~
    - デフォルトの表示位置は能登付近にする
  - [x] ~~地図にピンを立てる~~
  - [x] ~~ピン情報から緯度・経度を取得する~~
  - [x] ~~住民の位置をピンで表す~~
  - [x] ~~シミュレーション結果を表示する~~
  - [ ] 細かい調整する
    - スコアやペルソナに応じて、画像を入れ替える
- [ ] Backend
  - [ ] AIペルソナをn人分作る（本来は処理すべきだとデータセットで）
    - 緯度・経度情報に基づいたデータから作る
    - 衛星画像データを活用
    - 都度洗い替えではなく、いったんデータセットを作ってしまう
  - [x] ~~input: 緯度・経度・業態情報を受け取れるようにする~~
    - 業態：スーパーとか、最初は決め打ちで
  - [x] ~~output: あるAIペルソナがピン立てたところに行く行かないを判定~~
    - 0-1というよりはグラデーション（絶対行くなら10、絶対行かないなら0）
  - [ ] 並列処理できるようにする
- [x] ~~Infra~~
  - [x] ~~GCP~~
    - [x] ~~環境用意~~
    - [x] ~~プロモーションコードの適用~~
    - [x] ~~予算とアラートの設定~~
    - [x] ~~Google Map APIの設定~~
  - [x] AWS
    - [x] ~~環境用意~~
    - [x] ~~Lambda~~
    - [x] ~~API Gateway~~
    - [x] ~~DynamoDB~~
    - [x] ~~S3（画像用）~~
    - [x] ~~S3（フロント用）~~
      - （フロント用のS3は手動で作りました...すみません...）
- [ ] 発表準備
  - [ ] スライド作成
  - [x] ~~デモ環境準備~~
