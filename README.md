# food-navi

## 環境構築

- イメージの作成
  
```bash
docker-compose build
```


- パッケージインストール
  ```bash
  #初回
  docker-compose run --entrypoint "poetry install --no-root" chatbot

  #２回目以降
  docker-compose build --no-cache
  ```


- fastAPIの立ち上げ
```
docker-compose up chatbot
```
終了時は
CTRL+C 辺りを入力