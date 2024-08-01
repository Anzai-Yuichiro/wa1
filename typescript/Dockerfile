# ベースイメージを指定（ここではNode.jsの公式イメージを使用）
FROM node:18

# 作業ディレクトリを設定
WORKDIR /app

# パッケージ定義ファイルをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm install

# アプリケーションのソースコードをコピー
COPY . .

# TypeScriptをコンパイル
RUN npm run build

# アプリケーションを起動
CMD ["npm", "start"]

# コンテナがリッスンするポートを指定
EXPOSE 9000
