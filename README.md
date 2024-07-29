# HTTP通信を安全に行うHTTPSのハンズオン

## 事前準備
```sh
sudo apt update && sudo apt upgrade -y
sudo apt install -y openssl curl
```

dokcerをインストールしていない場合はインストールする．([ここを参照](https://docs.docker.com/engine/install/))

## (オレオレ)証明書の作成
certsディレクトリ内で行なっていく．

### 手順
1. サーバの秘密鍵の生成
2. 証明書署名要求(CSR)の生成
3. 自己証明書の生成

### 1. 秘密鍵の生成

秘密鍵の生成を行う．生成されるファイル名は`server.key`とする．

```sh
$ openssl genpkey -algorithm RSA -out server.key
```

- `genpkey`: 秘密鍵を生成(Generation of Private Key or Parameters)
- `-algorithm`: 署名アルゴリズム
- `-out`: 出力ファイル名を指定

### 2. 証明書署名要求(CSR)の生成
自分の秘密鍵から証明書を発行してもらうための証明書署名要求(CSR: Certicficate Signing Request)を`csr.pem`という名前で作成する．

```sh
$ openssl req -new -key server.key -out csr.pem
```

- `req`: 証明書署名要求を生成
- `-new`: 新しいCSRを作成
- `-key`: 秘密鍵を指定
- `-out`: 出力ファイル名を指定

```
# 入力例
-----
Country Name (2 letter code) [AU]: JP
State or Province Name (full name) [Some-State]: Hiroshima
Locality Name (eg, city) []: Hiroshima
Organization Name (eg, company) [Internet Widgits Pty Ltd]: ichipiroExplorer
Organizational Unit Name (eg, section) []: Development
Common Name (e.g. server FQDN or YOUR name) []: localhost
Email Address []: test@server.com
```

- Country Name: 国名をアルファベット2文字で表したもの([法務省より](https://www.moj.go.jp/MINJI/common_igonsyo/pdf/001321964.pdf))
- State or Province Name (full name): 州や省の名前(都道府県)
- Locality Name: 都市の名前(市町村名)
- Organization Name: 組織または会社名
- Organizational Unit Name: 組織内の部署名など
- Common Name: サーバのドメイン名またはFQDN(例: ichipiro.net, mail.example.com)
- Email Address: 管理者用のメールアドレス

### 3. 自己証明書の生成

秘密鍵と証明書署名要求から自己証明書を`server.crt`という名前で作成する．

```sh
$ openssl x509 -req -days 365 -in csr.pem -signkey ca-key.pem -out server.crt
```

- `x509`: Certificate display and signing command
- `-req`: CSRを使用して証明書を生成
- `-days`: 証明書の有効期間(n日間)
- `-in`: CSRを指定
- `-signkey`: 秘密鍵を指定
- `-out`: 出力ファイル名を指定


## Apache2(httpd)
自己証明書をcertsディレクトリからコピーする．

```sh
$ cp certs/server* apache2/
```

httpdのコンテナイメージを取得
```sh
$ docker image pull httpd:2.4
```

比較のためにHTTP通信のみのサーバを建てておく
```sh
$ docker run -d -p 50010:80 --name apache2-http httpd
```

このリポジトリ内にはすでに作成してあるが，https用のDockerfileと設定ファイルを作成する．

```Dockerfile
# Dockerfile
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
```

```.conf
# httpd-ssl.conf
Listen 443
<VirtualHost *:443>
    DocumentRoot "/usr/local/apache2/htdocs"
    ServerName localhost:443

    SSLEngine on
    SSLCertificateFile "/usr/local/apache2/conf/server.crt"
    SSLCertificateKeyFile "/usr/local/apache2/conf/server.key"

    <Directory "/usr/local/apache2/htdocs">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
```

httpdイメージを元にHTTPS通信をするdockerイメージを作成し，サーバを建てる．
```sh
$ docker build -t apache2-https .
$ docker run -d -p 50011:443 --name apache2-https apache2-https
```

アクセスしてみる．(ブラウザからでもok)
```sh
# http
curl http://localhost:50010

# https
curl --cacert server.crt https://localhost:50011
```

コンテナの停止と削除
```sh
$ docker stop apache2-http apache2-https
$ docker rm apache2-http apache2-https
$ docker image rm apache2-https
```

### 参考
- [docker hub  httpd Quick referrence](https://hub.docker.com/_/httpd)
- [Dockerのapche環境でHTTPSの設定](https://masaki-blog.net/docker-apache-https)


## nginx
自己証明書をcertsディレクトリからコピーする．

```sh
$ cp certs/server* nginx/
```

nginxのコンテナイメージを取得
```sh
$ docker image pull nginx:alpine
```

比較のためにHTTP通信のみのサーバを建てておく
```sh
$ docker run -d -p 50012:80 --name nginx-http nginx:alpine
```

このリポジトリ内にはすでに作成してあるが，https用のDockerfileと設定ファイルを作成する．

```Dockerfile
# Dockerfile
# ベースイメージを指定
FROM nginx:alpine

# 証明書と鍵の配置
COPY server.crt /etc/ssl/certs/server.crt
COPY server.key /etc/ssl/private/server.key

# Nginx設定ファイルの配置
COPY nginx.conf /etc/nginx/nginx.conf

# 自分のindex.htmlを配置する
COPY index.html /usr/share/nginx/html/index.html
```

```.conf
# nginx.conf
events {}

http {
    server {
        listen 443 ssl;
        server_name localhost;

        ssl_certificate /etc/ssl/certs/server.crt;
        ssl_certificate_key /etc/ssl/private/server.key;

        location / {
            root /usr/share/nginx/html;
            index index.html;
        }
    }
}
```

nginxイメージを元にHTTPS通信をするdockerイメージを作成し，サーバを建てる．
```sh
$ docker build -t nginx-https .
$ docker run -d -p 50013:443 --name nginx-https nginx-https
```

アクセスしてみる(ブラウザからでもok)
```sh
# http
curl http://localhost:50012

# https
curl --cacert server.crt https://localhost:50013
```

コンテナの停止と削除
```sh
$ docker stop nginx-http nginx-https
$ docker rm nginx-http nginx-https
$ docker image rm nginx-https
```
