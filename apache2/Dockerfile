# ベースイメージを指定
FROM httpd:2.4

# 証明書と鍵の配置
COPY server.crt /usr/local/apache2/conf/server.crt
COPY server.key /usr/local/apache2/conf/server.key

# SSLモジュールの有効化と設定の追加
RUN sed -i '/LoadModule ssl_module/s/^#//g' /usr/local/apache2/conf/httpd.conf && \
    sed -i '/Include conf\/extra\/httpd-ssl.conf/s/^#//g' /usr/local/apache2/conf/httpd.conf

# SSL設定ファイルの作成
COPY httpd-ssl.conf /usr/local/apache2/conf/extra/httpd-ssl.conf

# index.htmlの配置
COPY index.html /usr/local/apache2/htdocs/index.html
