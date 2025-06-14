#!/bin/bash

# スクリーンショット自動命名アプリのインストールスクリプト

echo "スクリーンショット自動命名アプリのセットアップを開始します..."

# Python 3が利用可能かチェック
if ! command -v python3 &> /dev/null; then
    echo "エラー: Python 3 がインストールされていません"
    echo "Homebrew を使用してインストールしてください: brew install python3"
    exit 1
fi

# 仮想環境を作成
echo "仮想環境を作成中..."
python3 -m venv venv

# 仮想環境をアクティベート
source venv/bin/activate

# パッケージをインストール
echo "依存関係をインストール中..."
pip install -r requirements.txt

# 実行権限を付与
chmod +x screenshot_namer.py

echo ""
echo "セットアップが完了しました！"
echo ""
echo "次の手順でアプリを使用できます:"
echo "1. .env ファイルを作成し、OpenAI API キーを設定してください"
echo "   cp .env.example .env"
echo "   vi .env"
echo ""
echo "2. アプリを実行してください:"
echo "   source venv/bin/activate"
echo "   python screenshot_namer.py"
echo ""
echo "または、バックグラウンドで実行:"
echo "   nohup python screenshot_namer.py > screenshot_namer.log 2>&1 &"