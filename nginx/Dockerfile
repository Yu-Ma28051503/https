# ベースイメージを指定
FROM nginx:alpine

# 証明書と鍵の配置
COPY server.crt /etc/ssl/certs/server.crt
COPY server.key /etc/ssl/private/server.key

# Nginx設定ファイルの配置
COPY nginx.conf /etc/nginx/nginx.conf

# 自分のindex.htmlを配置する
COPY index.html /usr/share/nginx/html/index.html
