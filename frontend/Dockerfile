# ベースイメージ
FROM node:20.9.0

# 作業ディレクトリの設定
WORKDIR /app

# 依存関係のインストール
COPY package.json package-lock.json ./
RUN npm install

# ポートの公開
EXPOSE 3000

# ホットリロードを有効にする
ENV CHOKIDAR_USEPOLLING=true

# 実行コマンド
CMD ["npm", "run", "dev"]
