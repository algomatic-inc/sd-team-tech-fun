# Team Tech Fun
Satellite Data Days ~ 衛星画像ハッカソン ~

Team Tech Funの開発リポジトリです

### イベントURL
https://lu.ma/vnnro5q4?tk=olCl0z

## 🤖 技術要素
![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white&style=flat)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white&style=flat)
![Google Cloud](https://img.shields.io/badge/Google%20Cloud-%234285F4.svg?style=for-the-badge&logo=google-cloud&logoColor=white&style=flat)
![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-web-services&logoColor=white&style=flat)

## 📁 フォルダ構成
```bash
$ tree
.
├── README.md
├── credentials
└── samples
    ├── README.md
    ├── hello_gemini
    │   └── hello_genimi.py
    ├── hello_genimi.py
    ├── pyproject.toml
    └── uv.lock
```

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
```bash
cdk synth
cdk deploy
```

対象のAWSアカウントは別途管理

## 🎯 機能
現在検討中...

## 💡 テーマ
​未来の都市と社会を創造するデジタルツール

## ⚠️ 制限事項
- ご提供されているデータの取扱いに注意すること
- ご提供されているAPIの取扱いに注意すること

## ✅ TODO
(GitHub Project作れなかった...)
- [ ] 技術検証
  - [x] ~~Gemini呼び出し~~
  - [x] ~~提供されたAPIの呼び出し~~
  - [ ] xxx
- [ ] Frontend
  - [ ] xxx
- [ ] Backend
  - [ ] xxx
- [ ] Infra
  - [ ] GCP
    - [x] ~~環境用意~~
    - [x] ~~プロモーションコードの適用~~
    - [x] ~~予算とアラートの設定~~
  - [ ] AWS
    - [x] ~~環境用意~~
    - [ ] infraフォルダにcdk
