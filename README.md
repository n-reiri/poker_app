# Poker App (テキサスホールデム チップ管理 Webアプリ)

## 概要

対面で行うテキサスホールデムポーカーのチップ管理をWeb上で行うアプリケーションです。スマホ・タブレット・PCのブラウザから、部屋作成・参加、リアルタイムなチップ交換、アクション履歴、最終チップ集計までをサポートします。

## 主な機能

* ユーザー登録（サインアップ）／ログイン／ログアウト
* 部屋（Room）の作成・一覧表示
* 部屋への参加（ホスト・参加者制御）
* リアルタイムチップ管理（WebSocket／Django Channels）
* アクション履歴（Bet, Call, Check, Fold, Raise）
* ゲーム結果のチップ順位表示

## 技術スタック

* Python 3.9+
* Django 5.x
* Django Channels (WebSocket)
* SQLite（開発用）→ PostgreSQL（本番想定）
* HTML/CSS (Django テンプレート + static ファイル)
* JavaScript（WebSocket 通信）

## 環境構築手順

1. リポジトリをクローン

   ```bash
   git clone <リポジトリURL>
   cd poker_app_dev
   ```
2. 仮想環境の作成・有効化

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```
3. 依存関係のインストール

   ```bash
   pip install -r requirements.txt
   ```
4. マイグレーション実行

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. スーパーユーザー作成

   ```bash
   python manage.py createsuperuser
   ```
6. 開発サーバー起動

   ```bash
   python manage.py runserver
   ```
7. ブラウザでアクセス

   * [http://127.0.0.1:8000/](http://127.0.0.1:8000/) （ログイン／サインアップ画面）
   * サインアップ後またはスーパーユーザーでログインし、部屋一覧へ

## ディレクトリ構成

```
poker_app_dev/
├── manage.py
├── db.sqlite3
├── requirements.txt
├── poker_app/        # プロジェクト設定
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
└── game/             # アプリ本体
    ├── models.py     # Room, Player, Action
    ├── views.py      # ログイン／サインアップ／部屋一覧／ゲーム等
    ├── consumers.py  # WebSocket コンシューマ
    ├── routing.py    # WebSocket ルーティング
    ├── urls.py       # アプリ URLconf
    ├── templates/    # HTML テンプレート
    └── static/       # CSS/JS
```

## 開発ルール

* コーディングスタイル: PEP8 準拠
* フロントエンド: TailwindCSS やフレームワーク導入は要相談
* コミットメッセージ: feat/fix/docs のプリフィックスを付与

## 貢献方法

1. Fork → ブランチ作成 (`feature/xxx`, `fix/xxx`)
2. 実装 → テスト → PR 作成
3. コードレビュー後、main へマージ

## ライセンス

MIT ライセンス

