# AITAC_step2
研修用勤怠アプリ

- Pythonとpythonのパッケージ管理モジュールpipのインストール
```sh
sudo apt update
sudo apt install python3 
sudo apt install python3-pip
```
や
```sh
sudo yum -y update
sudo yum install python3
sudo yum install python3-pip
```

- gitのインストール
```sh
sudo apt install git
```
など

- 適当に作業用フォルダを作成
```sh
mkdir deployed_app
```

- 作業用フォルダ以下にappをpull
```sh
cd deployed_app
git init
git pull https://github.com/FujiwaraDaigo/AITAC_step2_kintai_app.git
```

- pythonの依存ライブラリ(flask,その他)のインストール
```sh
pip3 install -r requirements.txt
```

- データベース(sqlite3)の初期化
```sh
python3 migrate.py
```

- アプリケーションの起動
```sh
python3 app.py
```