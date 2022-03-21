import os
import mysql.connector


# DB接続情報
def conn_db():
    conn = mysql.connector.connect(
        host="192.168.5.129",  # localhostでもOK
        user="app_server",
        passwd="It@cstep2",
        db="app_database",
    )
    return conn


conn = conn_db()
c = conn.cursor()

print("Do you want to remove current database? (y/n)")
if input() == "y" or input() == "Y":
    # テーブルの初期化
    c.execute("""drop table user""")
    c.execute("""drop table kintai""")


# ユーザーテーブルの作成
c.execute(
    """create table user(
        user_id integer NOT NULL,
        password_hash text NOT NULL
    )"""
)

# ユーザーテーブルの作成
c.execute(
    """create table kintai(
        record_id integer PRIMARY KEY AUTO_INCREMENT,
        user_id integer NOT NULL,
        created_at text NOT NULL,
        start_or_end text NOT NULL
    )"""
)


conn.commit()
conn.close()
