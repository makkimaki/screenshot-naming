#!/usr/bin/env python3
"""
スクリーンショット自動命名アプリ

macOSでスクリーンショットが撮影されたときに、
画像の内容を解析して自動的にファイル名を変更するアプリケーション
"""

import os
import re
import time
from pathlib import Path
from datetime import datetime
import base64
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from openai import OpenAI
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

class ScreenshotHandler(FileSystemEventHandler):
    """スクリーンショットファイルの監視と処理を行うクラス"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.screenshot_dir = Path(os.getenv('SCREENSHOT_DIR', os.path.expanduser('~/Desktop')))
        self.language = os.getenv('LANGUAGE', 'ja')
        
        # macOSのスクリーンショットファイル名パターン
        self.screenshot_pattern = re.compile(r'スクリーンショット\s\d{4}-\d{2}-\d{2}\s\d{1,2}\.\d{2}\.\d{2}\.png')
        
        print(f"監視ディレクトリ: {self.screenshot_dir}")
        print(f"言語設定: {self.language}")
    
    def on_created(self, event):
        """新しいファイルが作成されたときの処理"""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # スクリーンショットファイルかどうかチェック
        if self.is_screenshot_file(file_path):
            print(f"スクリーンショットを検出: {file_path.name}")
            # ファイルの書き込みが完了するまで少し待機
            time.sleep(1)
            self.process_screenshot(file_path)
    
    def is_screenshot_file(self, file_path):
        """ファイルがスクリーンショットかどうか判定"""
        return (file_path.suffix.lower() == '.png' and 
                self.screenshot_pattern.match(file_path.name))
    
    def encode_image(self, image_path):
        """画像をbase64エンコード"""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"画像エンコードエラー: {e}")
            return None
    
    def analyze_image(self, image_path):
        """画像を解析してファイル名を生成"""
        try:
            # 画像をbase64エンコード
            base64_image = self.encode_image(image_path)
            if not base64_image:
                return None
            
            # OpenAI GPT-4 Vision APIを使用して画像を解析
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"この画像の内容を簡潔に説明して、適切なファイル名を{self.language}で提案してください。ファイル名は20文字以内で、特殊文字は使わず、内容が分かりやすいものにしてください。拡張子は含めないでください。"
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=100
            )
            
            # レスポンスからファイル名を抽出
            suggested_name = response.choices[0].message.content.strip()
            
            # ファイル名として使用できない文字を除去
            clean_name = re.sub(r'[^\w\s-]', '', suggested_name)
            clean_name = re.sub(r'\s+', '_', clean_name)
            clean_name = clean_name[:20]  # 20文字以内に制限
            
            return clean_name
            
        except Exception as e:
            print(f"画像解析エラー: {e}")
            return None
    
    def process_screenshot(self, file_path):
        """スクリーンショットを処理してファイル名を変更"""
        try:
            print(f"画像を解析中: {file_path.name}")
            
            # 画像を解析してファイル名を生成
            new_name = self.analyze_image(file_path)
            
            if new_name:
                # 新しいファイルパスを作成
                new_file_path = file_path.parent / f"{new_name}.png"
                
                # 同名ファイルが存在する場合は番号を追加
                counter = 1
                while new_file_path.exists():
                    new_file_path = file_path.parent / f"{new_name}_{counter}.png"
                    counter += 1
                
                # ファイル名を変更
                file_path.rename(new_file_path)
                print(f"ファイル名を変更: {file_path.name} -> {new_file_path.name}")
            else:
                print("ファイル名の生成に失敗しました")
                
        except Exception as e:
            print(f"ファイル処理エラー: {e}")

def main():
    """メイン実行関数"""
    print("スクリーンショット自動命名アプリを開始します...")
    
    # 必要な環境変数をチェック
    if not os.getenv('OPENAI_API_KEY'):
        print("エラー: OPENAI_API_KEY が設定されていません")
        print(".env ファイルを作成して OpenAI API キーを設定してください")
        return
    
    # イベントハンドラーとオブザーバーを設定
    event_handler = ScreenshotHandler()
    observer = Observer()
    observer.schedule(event_handler, str(event_handler.screenshot_dir), recursive=False)
    
    # 監視開始
    observer.start()
    print(f"スクリーンショット監視を開始しました (Ctrl+C で終了)")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nアプリケーションを終了します...")
        observer.stop()
    
    observer.join()
    print("終了しました")

if __name__ == "__main__":
    main()