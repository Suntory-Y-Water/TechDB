# tech-db-backend

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

# テスト
docker-compose run --entrypoint "poetry run pytest" fast-api


```
## その他

``` bash

docker compose stop

docker compose down
```
