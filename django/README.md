``` bash

cd django
mkdir .dockervenv

docker compose build

docker compose run --entrypoint "poetry install --no-root" django-backend

# 依存パッケージの再ビルド
docker-compose build --no-cache

# コンテナの起動
docker compose up -d

```