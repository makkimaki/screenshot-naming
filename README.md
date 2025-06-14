# スクリーンショット自動命名アプリ

macOSでスクリーンショットを撮影したときに、画像の内容を自動解析してファイル名を変更するアプリケーションです。

## 機能

- スクリーンショットファイルの自動検出
- OpenAI GPT-4 Vision APIを使用した画像内容の解析
- 内容に基づいた適切なファイル名の自動生成
- バックグラウンドでの常駐監視

## 必要な環境

- macOS
- Python 3.8以上
- OpenAI API キー

## インストール方法

1. リポジトリをクローンまたはダウンロード
2. インストールスクリプトを実行:
   ```bash
   ./install.sh
   ```

3. 環境設定ファイルを作成:
   ```bash
   cp .env.example .env
   ```

4. `.env` ファイルを編集してOpenAI API キーを設定:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   SCREENSHOT_DIR=/Users/your_username/Desktop
   LANGUAGE=ja
   ```

## 使用方法

### 基本的な実行

```bash
# 仮想環境をアクティベート
source venv/bin/activate

# アプリを実行
python screenshot_namer.py
```

### バックグラウンド実行

```bash
# バックグラウンドで実行（ログファイルに出力）
nohup python screenshot_namer.py > screenshot_namer.log 2>&1 &
```

### プロセス確認・終了

```bash
# 実行中のプロセスを確認
ps aux | grep screenshot_namer

# プロセスを終了
kill <プロセスID>
```

## 設定項目

`.env` ファイルで以下の項目を設定できます:

- `OPENAI_API_KEY`: OpenAI API キー（必須）
- `SCREENSHOT_DIR`: スクリーンショットが保存されるディレクトリ（デフォルト: ~/Desktop）
- `LANGUAGE`: ファイル名生成言語（デフォルト: ja）

## 動作原理

1. 指定されたディレクトリ（デフォルト: デスクトップ）を監視
2. macOSのデフォルトスクリーンショットファイル名パターンを検出
3. 新しいスクリーンショットが作成されたらOpenAI GPT-4 Vision APIで画像を解析
4. 解析結果に基づいて適切なファイル名を生成
5. 元のスクリーンショットファイルの名前を変更

## 注意事項

- OpenAI API の使用には料金が発生します
- インターネット接続が必要です
- macOSのスクリーンショット機能で撮影された画像のみ対象です

## トラブルシューティング

### よくある問題

1. **API キーエラー**
   - `.env` ファイルが正しく設定されているか確認
   - OpenAI API キーが有効か確認

2. **ファイルが検出されない**
   - `SCREENSHOT_DIR` が正しいパスか確認
   - macOSのスクリーンショット設定を確認

3. **権限エラー**
   - ファイルの読み書き権限を確認
   - 必要に応じて `chmod` でアクセス権を変更