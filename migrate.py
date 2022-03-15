import os
import sqlite3

print("remove OK? if OK pless y")
if os.path.exists("db.sqlite3") and input() == "y":
    os.remove("db.sqlite3")

conn = sqlite3.connect("db.sqlite3")
c = conn.cursor()

# ポートフォリオテーブルの作成
c.execute(
    """create table portfolio(
        portfolio_id integer,
        stock_name text NOT NULL,
        image_path text NOT NULL
    )"""
)

# ユーザーテーブルの作成
c.execute(
    """create table user(
        user_id integer,
        password text NOT NULL
    )"""
)


conn.commit()
conn.close()
