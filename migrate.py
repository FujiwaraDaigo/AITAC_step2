import os
import sqlite3

print("remove OK? if OK pless y")
if os.path.exists("db.sqlite3") and input() == "y":
    os.remove("db.sqlite3")

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

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
        record_id integer PRIMARY KEY AUTOINCREMENT,
        user_id integer NOT NULL,
        created_at text NOT NULL,
        start_or_end text NOT NULL
    )"""
)


conn.commit()
conn.close()
