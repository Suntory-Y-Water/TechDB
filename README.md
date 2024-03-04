# tech-db

## backend

``` bash

cd backend
mkdir .dockervenv

# ビルドしてイメージの作成
docker compose build

# 依存パッケージのダウンロード
docker-compose run --entrypoint "poetry install --no-root" fast-api

# 依存パッケージの再ビルド
docker-compose build --no-cache

# コンテナの起動
docker compose up -d

# データベースの初期化
docker-compose exec fast-api poetry run python -m api.migrate_db

# ブログを追加する
http://localhost:8000/docs#/default/create_blog_blog_post へアクセスして、よしなに追加する。

uuidを主キーにしているため、適当にやっても追加される


```

## frontend

``` bash

# コンテナの起動(すでに起動している場合、http://localhost:3000/へアクセスする)
docker compose up -d

# http://localhost:3000/check へアクセスし、APIが叩けているかチェック
エラーが発生した場合は、**ブログを追加する**セクションを参考
```

## その他

**Fast APIとNext.jsで疎通チェックを行ったが、Djangoに変更する可能性あり**

``` bash

docker compose stop

docker compose down
```
