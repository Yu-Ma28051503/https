FROM httpd:latest

# コンテナの更新
RUN apt-get update

# SSL通信をするための設定を有効にする
RUN sed -i \
		-e 's/^#\(Include .*httpd-ssl.conf\)/\1/' \
		-e 's/^#\(LoadModule .*mod_ssl.so\)/\1/' \
		-e 's/^#\(LoadModule .*mod_socache_shmcb.so\)/\1/' \
		conf/httpd.conf

# 必要なファイルのコピー 
COPY index.html /usr/local/apache2/htdocs/
# COPY apache.conf /usr/local/apache2/conf/httpd.conf
COPY certs/server.crt certs/server.key /usr/local/apache2/conf/
