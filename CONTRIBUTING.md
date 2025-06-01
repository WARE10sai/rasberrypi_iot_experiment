# 貢献ガイドライン

このプロジェクトへの貢献をありがとうございます！以下のガイドラインに従って、プロジェクトに貢献してください。

## 始め方

1. このリポジトリをフォークしてください
2. ローカルにクローンしてください:
   ```bash
   git clone https://github.com/yourusername/rasberrypi_iot_experiment.git
   cd rasberrypi_iot_experiment
   ```
3. 仮想環境を作成・有効化してください:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   ```
4. 開発用依存関係をインストールしてください:
   ```bash
   pip install -r requirements-dev.txt
   ```

## 開発ワークフロー

### 1. ブランチの作成

機能追加やバグ修正のため、新しいブランチを作成してください:

```bash
git checkout -b feature/新機能名
# または
git checkout -b bugfix/バグ修正名
```

### 2. コードの品質

コードをコミットする前に、以下のツールを実行してください:

```bash
# コードフォーマット
black .
isort .

# リンター
flake8 .

# 型チェック
mypy .

# テスト
pytest
```

### 3. コミットメッセージ

明確で説明的なコミットメッセージを書いてください:

```
feat: センサーデータのキャッシュ機能を追加

- Redis を使用したキャッシュ機能を実装
- API応答時間を改善
- 設定可能なキャッシュ有効期限を追加
```

コミットメッセージの形式:
- `feat:` 新機能
- `fix:` バグ修正
- `docs:` ドキュメントの変更
- `style:` コードスタイルの変更
- `refactor:` リファクタリング
- `test:` テストの追加・修正
- `chore:` その他の変更

### 4. テスト

新しい機能やバグ修正には、適切なテストを追加してください:

```bash
# 新しいテストファイルを作成
touch tests/test_new_feature.py

# テストを実行
pytest tests/test_new_feature.py
```

### 5. Pull Request

1. 変更をリモートブランチにプッシュしてください:
   ```bash
   git push origin feature/新機能名
   ```

2. GitHubでPull Requestを作成してください

3. Pull Requestには以下を含めてください:
   - 変更内容の明確な説明
   - 関連するIssue番号（あれば）
   - テスト結果のスクリーンショット（UI変更の場合）

## コーディング規約

### Python

- [PEP 8](https://pep8.org/) に従ってください
- 関数とクラスには適切なdocstringを追加してください
- 型ヒントを使用してください（Python 3.7+）

### ファイル構造

```
rasberrypi_iot_experiment/
├── main.py              # FastAPIアプリケーション
├── sensors/             # センサー関連モジュール
├── web/                 # Web関連モジュール
├── tests/               # テストファイル
├── docs/                # ドキュメント
└── requirements*.txt    # 依存関係
```

## バグレポート

バグを発見した場合は、以下の情報を含めてIssueを作成してください:

1. **環境情報**:
   - OS (Raspberry Pi OS バージョン)
   - Python バージョン
   - 依存関係のバージョン

2. **再現手順**:
   1. 具体的な手順
   2. 期待される結果
   3. 実際の結果

3. **エラーメッセージ**:
   - 完全なトレースバック
   - ログファイル（可能であれば）

## 機能要求

新機能の提案は歓迎します！Issueテンプレートを使用して以下を含めてください:

1. **動機**: なぜこの機能が必要か
2. **詳細な説明**: 機能の動作方法
3. **実装案**: 可能であれば実装のアイデア
4. **代替案**: 他の解決方法があれば

## 質問とサポート

質問がある場合は:

1. まず既存のIssueを検索してください
2. [Discussions](https://github.com/yourusername/rasberrypi_iot_experiment/discussions) を使用してください
3. 新しいIssueを作成してください

## ライセンス

このプロジェクトに貢献することで、あなたの貢献がMITライセンスの下でライセンスされることに同意したものとみなされます。 