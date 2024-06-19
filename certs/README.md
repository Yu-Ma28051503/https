# (オレオレ)証明書の作成手順

## 概要


## 手順

1. 秘密鍵の生成
2. 証明書署名要求(CSR)の生成
3. 自己証明書の生成

## 1. 秘密鍵の生成

秘密鍵の生成を行う．生成されるファイル名は`key.pem`とする．

```bash
$ openssl genpkey -algorithm RSA -out key.pem
```

- `genpkey`: 秘密鍵を生成(Generation of Private Key or Parameters)
- `-algorithm`: 署名アルゴリズム
- `-out`: 出力ファイル名を指定

## 2. 証明書署名要求(CSR)の生成

自分の秘密鍵から証明書を発行してもらうための証明書署名要求(CSR: Certicficate Signing Request)を`csr.pem`という名前で作成する．

```
openssl req -new -key key.pem -out csr.pem
```

- `req`: 証明書署名要求を生成
- `-new`: 新しいCSRを作成
- `-key`: 秘密鍵を指定
- `-out`: 出力ファイル名を指定

コマンドを実行するといろんな情報が聞かれるので入力していく．
```
# 入力例
-----
Country Name (2 letter code) [AU]:JP
State or Province Name (full name) [Some-State]:Hiroshima
Locality Name (eg, city) []:Hiroshima
Organization Name (eg, company) [Internet Widgits Pty Ltd]:ichipiro
Organizational Unit Name (eg, section) []:Development
Common Name (e.g. server FQDN or YOUR name) []:localhost
Email Address []:test@example.com
```

- Country Name: 国名をアルファベット2文字で表したもの([法務省より](https://www.moj.go.jp/MINJI/common_igonsyo/pdf/001321964.pdf))
- State or Province Name (full name): 州や省の名前(都道府県)
- Locality Name: 都市の名前(市町村名)
- Organization Name: 組織または会社名
- Organizational Unit Name: 組織内の部署名など
- Common Name: サーバのドメイン名またはFQDN(例: ichipiro.net, mail.example.com)
- Email Address: 管理者用のメールアドレス

## 自己証明書の生成

秘密鍵と証明書署名要求から自己証明書を`cert.pem`という名前で作成する．

```
openssl x509 -req -days 365 -in csr.pem -signkey key.pem -out cert.pem
```

- `x509`: Certificate display and signing command
- `-req`: CSRを使用して証明書を生成
- `-days`: 証明書の有効期間(n日間)
- `-in`: CSRを指定
- `-signkey`: 秘密鍵を指定
- `-out`: 出力ファイル名を指定
