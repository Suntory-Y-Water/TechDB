# chatbot

## 環境構築(構築済みで不要)

- イメージの作成
  
```bash
docker-compose build
```

- poetryによるPython環境のセットアップ
```bash
docker-compose run \
  --entrypoint "poetry init \
    --name chatbot\
    --dependency fastapi \
    --dependency uvicorn[standard]" \
  chatbot
```


- パッケージインストール
  ```bash
  docker-compose run --entrypoint "poetry install --no-root" chatbot
  ```


- fastAPIの立ち上げ
```
docker-compose up
```
下記にアクセス
http://localhost:8000/docs


引用元
https://zenn.dev/sh0nk/books/537bb028709ab9/viewer/bdf8a5