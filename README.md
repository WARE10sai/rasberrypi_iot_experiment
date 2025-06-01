# Raspberry Pi Sense HAT Sensor API

Raspberry PiのSense HATセンサーからのデータ（温度、湿度、気圧）を提供するFastAPIベースのWebアプリケーションです。

## 機能

- **リアルタイムセンサーデータ取得**: 温度、湿度、気圧の読み取り
- **データ履歴管理**: SQLiteデータベースを使用した履歴保存
- **Web UI**: シンプルなWebインターフェース
- **REST API**: JSON形式でのデータ提供
- **LED制御**: 温度に応じたLEDマトリックスの色制御

## 必要な環境

- Raspberry Pi（Sense HAT搭載）
- Python 3.7+
- Sense HAT library

## インストール

1. リポジトリをクローン:
```bash
git clone <repository-url>
cd raspberrypi_iot_experiment
```

2. 仮想環境を作成・有効化:
```bash
# システムのパッケージ（RTIMUなど）を仮想環境内で使用できるようにする
python -m venv venv --system-site-packages
source venv/bin/activate  # Linux/Mac
# または
venv\Scripts\activate     # Windows
```

3. 依存関係をインストール:
Raspberry Pi環境 (Sense HAT搭載):
```bash
# システムパッケージをインストール
sudo apt-get update
sudo apt-get install -y sense-hat
sudo apt-get install -y python3-rtimulib

# Pythonパッケージをインストール
pip install -r requirements.txt
```

開発環境 (Mac/Windowsなど) ではSense HATが不要:
```bash
pip install -r requirements-dev.txt
```

## 使用方法

### サーバーの起動

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### API エンドポイント

#### センサーデータ取得
```
GET /sensors
```

レスポンス例:
```json
{
  "temperature": 25.3,
  "humidity": 45.2,
  "pressure": 1013.25
}
```

#### データ履歴取得
```
GET /history?limit=50
```

レスポンス例:
```json
[
  {
    "ts": "2024-01-01T12:00:00",
    "temperature": 25.3,
    "humidity": 45.2,
    "pressure": 1013.25
  }
]
```

#### Web UI
```
GET /
```

メインのWebインターフェースにアクセス

## プロジェクト構造

```
raspberrypi_iot_experiment/
├── main.py              # FastAPIメインアプリケーション
├── sensors/
│   └── temp.py          # Sense HATセンサー制御モジュール
├── web/
│   ├── templates/       # HTMLテンプレート
│   ├── web.py          # Web関連ユーティリティ
│   └── db.py           # データベース関連
├── sensors.db          # SQLiteデータベース
├── requirements.txt    # Python依存関係
└── README.md          # このファイル
```

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 作者

- **Takumi Ishida** - *Initial work*

## 謝辞

- Raspberry Pi Foundationのドキュメントとコミュニティ
- Sense HATライブラリの開発者の皆様
- FastAPIフレームワークの開発チーム

## トラブルシューティング

### RTIMUモジュールが見つからないエラー

`ModuleNotFoundError: No module named 'RTIMU'` というエラーが発生した場合、以下の方法を試してください：

1. 既存の仮想環境を削除して、システムパッケージを利用する新しい仮想環境を作成:
```bash
# 仮想環境を抜ける
deactivate
# 既存の仮想環境を削除
rm -rf venv
# システムサイトパッケージを利用する仮想環境を作成
python -m venv venv --system-site-packages
# 仮想環境を有効化
source venv/bin/activate
# 依存関係をインストール
pip install -r requirements.txt
```

2. または、仮想環境を使わずに直接実行:
```bash
# システム全体にパッケージをインストール
sudo pip3 install -r requirements.txt
# 仮想環境なしで実行
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### websocketsモジュールが見つからないエラー

`ModuleNotFoundError: No module named 'websockets.legacy.handshake'` というエラーが発生した場合：

```bash
# websocketsパッケージを明示的にインストール
pip install websockets>=10.0

# uvicornを標準オプション付きで再インストール
pip install uvicorn[standard]
```

または、requirements.txtを更新して再インストールすることもできます：

```bash
# requirements.txtの更新後、再度インストール
pip install -r requirements.txt
```