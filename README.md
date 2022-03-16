# AITAC_step2
研修用勤怠アプリ

- Pythonとpythonのパッケージ管理モジュールpipのインストール
```sh
sudo apt update
sudo apt install python3
```
や
```sh
sudo yum -y update
sudo yum install python3
```

- ディレクトリに移動
```sh
cd AITAC_step2_kintai_app
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