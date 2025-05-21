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
# ポーカーアプリ プロジェクト概要

このドキュメントでは、`poker_app_dev/` プロジェクト配下のディレクトリ構造と、各ファイル／フォルダの役割を具体的に解説します。

---

## プロジェクトルート

```
poker_app_dev/                # プロジェクトルートフォルダ
├── venv/                      # Python 仮想環境
├── manage.py                  # Django 管理コマンド用スクリプト
├── db.sqlite3                 # 開発用 SQLite データベース
├── poker_app/                 # Django プロジェクト設定フォルダ
└── game/                      # ポーカーアプリ本体アプリフォルダ
```

### `venv/`

* Python の仮想環境 (dependencies を分離管理)

### `manage.py`

* Django 管理コマンドを実行 (例: `runserver`, `migrate`, `createsuperuser`)

### `db.sqlite3`

* 開発時に使うデフォルトの SQLite データベースファイル

---

## プロジェクト設定 (`poker_app/`)

```
poker_app/
├── __init__.py
├── asgi.py                   # ASGI (Channels, WebSocket) 用エントリポイント
├── settings.py               # プロジェクト全体設定 (言語設定、DB、CHANNEL_LAYERS etc.)
├── urls.py                   # プロジェクトルーティング (admin/, accounts/, game/)
└── wsgi.py                   # WSGI (HTTP) 用エントリポイント
```

* **`settings.py`**

  * `INSTALLED_APPS` に `game`, `channels`, `django.contrib.auth` などを登録
  * 言語: `LANGUAGE_CODE = 'ja'`
  * タイムゾーン: `TIME_ZONE = 'Asia/Tokyo'`
  * メッセージ設定: `MESSAGE_STORAGE`
  * 認証リダイレクト: `LOGIN_REDIRECT_URL`, `LOGOUT_REDIRECT_URL`
  * Channels: `ASGI_APPLICATION`, `CHANNEL_LAYERS`

* **`urls.py`**

  * `path('admin/', admin.site.urls)`
  * `path('accounts/', include('django.contrib.auth.urls'))`
  * `path('', include('game.urls'))`

* **`asgi.py`**

  * HTTP と WebSocket を振り分ける `ProtocolTypeRouter`
  * `game.routing.websocket_urlpatterns` を読み込み

* **`wsgi.py`**

  * 本番環境での HTTP リクエスト受付用エントリポイント

---

## アプリケーション本体 (`game/`)

```
game/
├── __init__.py
├── admin.py                  # Django 管理画面へのモデル登録
├── apps.py                   # アプリケーション設定 (name = 'game')
├── models.py                 # DBモデル定義: Room, Player, Action
├── migrations/               # マイグレーション履歴
├── views.py                  # 各種ビューの実装
├── urls.py                   # アプリ固有の URLconf
├── routing.py                # WebSocket ルーティング定義
├── consumers.py              # Channels コンシューマ (非同期 WebSocket 処理)
├── templates/                # テンプレートフォルダ
│   ├── game/                 # ゲーム画面関連
│   │   ├── base.html         # 共通レイアウト
│   │   ├── home.html         # ログインフォーム
│   │   ├── room_list.html    # 部屋一覧・作成・参加画面
│   │   ├── game.html         # ゲームテーブル画面
│   │   └── results.html      # 結果集計画面
│   └── registration/         # 認証関連
│       ├── login.html        # ログイン画面
│       ├── signup.html       # 新規登録フォーム
│       ├── signup_success.html # 登録完了ページ
│       └── logged_out.html   # ログアウト完了ページ
└── static/                   # 静的ファイルフォルダ
    └── game/
        ├── css/
        │   └── style.css     # 全体スタイル定義
        └── js/
            └── app.js        # WebSocket, DOM 更新, イベントハンドラ
```

### `models.py`

* **Room**: ゲーム部屋 (name, host, created\_at, is\_active)
* **Player**: 部屋参加者 (外部キー: Room & User, 現在チップ数, is\_dealer)
* **Action**: プレイヤーのアクション履歴 (bet/fold/call/check/raise, amount)

### `admin.py`

* `admin.site.register(Room)`, `admin.site.register(Player)`, `admin.site.register(Action)` で管理画面に表示可能

### `views.py`

* **home**: 未ログイン時に `AuthenticationForm` を処理しログイン、成功で `room_list` へ。
* **signup**: `UserCreationForm` で新規登録し即ログイン→ `room_list` へ+ メッセージ表示。
* **room\_list**: 自分がホストの部屋一覧表示 + 新規作成処理。
* **join\_room**: POST のみで参加登録 (ホスト自身または既参加者のみ)。
* **game**: ホスト or 参加者のみゲーム画面表示 (players, room\_id を渡す)。
* **results**: 最終チップ数順にソートして結果画面表示。

### `urls.py` (app)

* `/` → `home`
* `/signup/` → `signup`
* `/rooms/` → `room_list`
* `/rooms/<id>/join/` → `join_room`
* `/rooms/<id>/` → `game`
* `/rooms/<id>/results/` → `results`

### `routing.py` & `consumers.py`

* WebSocket の接続先パス: `ws://<host>/ws/rooms/<room_id>/`
* **GameConsumer**:

  1. `connect`: グループ参加
  2. `receive`: JSON データ受信→`update_player_and_record` により DB 更新 & Action 登録→グループブロードキャスト
  3. `broadcast_message`: クライアント全員に更新情報送信
  4. `disconnect`: グループ離脱

### テンプレート

* **base.html**: 全ページ共通ヘッダー(ログイン/ユーザー名/ログアウト)、フッター、CSS/JS 読み込み
* **home.html**: ログインフォーム (フォーム送信先 `/`)
* **registration/login.html**: `LoginView` 用ログインフォーム
* **registration/signup.html**: 新規登録フォーム
* **signup\_success.html**: 登録完了メッセージ+自動リダイレクト
* **logged\_out.html**: ログアウト完了画面
* **room\_list.html**: 部屋一覧 (作成済み、参加中、参加可能) + 作成/参加フォーム
* **game.html**: テーブル俯瞰、プレイヤーリスト、アクションパネル、`<script id="room-id">` に JSON room\_id
* **results.html**: プレイヤー毎の最終チップ数表形式

### 静的ファイル

* **style.css**: フォント、ボタン、リスト、メッセージ、レイアウト調整
* **app.js**: WebSocket 接続、onmessage でチップ数更新、アクションボタン送信イベント

---

以上が各ファイルの詳細な役割説明です。プロジェクトに参加される方は、目的の機能に合わせて該当ファイルを編集してください。


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

