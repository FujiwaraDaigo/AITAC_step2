import sqlite3
import hashlib
import datetime
import mysql.connector


class DataBase:
    def __init__(self, db="db.sqlite3"):
        self.db = db

    def register_user(self, user_id: int, password: str):
        result = self.load_user(user_id=user_id)
        if len(result) == 0:
            password_hash = hashlib.md5(password.encode("utf-8")).hexdigest()

            with sqlite3.connect(self.db) as con:
                c = con.cursor()
                q = f"""
                                insert into user(user_id, password_hash) values(
                                    {user_id}, '{password_hash}'
                                )
                            """
                print(q)
                c.execute(q)
                con.commit()
            return q
        else:
            return "already_exist"

    def register_kintai(
        self,
        user_id: int,
        start_or_end: str,
        created_at: str = "now",
    ):
        if created_at == "now":
            dt_now = datetime.datetime.now()
            created_at = dt_now.strftime("%Y/%m/%d/%H:%M:%S")

        with sqlite3.connect(self.db) as conn:
            c = conn.cursor()
            q = f"""
                            insert into kintai(user_id, created_at, start_or_end) values(
                                {user_id}, '{created_at}', '{start_or_end}' 
                            )
                        """
            print(q)
            c.execute(q)
            conn.commit()

        return q

    def load_user(self, user_id: int):

        with sqlite3.connect("db.sqlite3") as conn:
            c = conn.cursor()
            q = f"SELECT * FROM user WHERE user_id={user_id}"
            c.execute(q)
            user_info = c.fetchall()

        return user_info

    def load_kintai(self, user_id: int):

        with sqlite3.connect("db.sqlite3") as conn:
            c = conn.cursor()
            q = f"SELECT * FROM kintai WHERE user_id={user_id} ORDER BY created_at ASC"
            c.execute(q)
            kintai_info = c.fetchall()

        return kintai_info

    def load_record(self, record_id: int):

        with sqlite3.connect("db.sqlite3") as conn:
            c = conn.cursor()
            q = f"SELECT * FROM kintai WHERE record_id={record_id}"
            c.execute(q)
            record_info = c.fetchall()

        return record_info

    def check_user_password(self, user_id: int, password: str):
        user_info = self.load_user(user_id=user_id)
        if len(user_info) > 1:
            raise Exception("userデータベースがユニークでありません")
        elif len(user_info) == 0:
            return 0
        else:
            user_id, password_hash = user_info[0]
            password_hash2 = hashlib.md5(password.encode("utf-8")).hexdigest()
            if password_hash == password_hash2:
                return 1
            else:
                return -1

    def remove_record(self, record_id: int):
        with sqlite3.connect("db.sqlite3") as conn:
            c = conn.cursor()
            q = f"DELETE FROM kintai WHERE record_id={record_id}"
            print(q)
            c.execute(q)
            conn.commit()

        return q

    def edit_record(self, record_id: int, created_at: str, start_or_end: str):
        with sqlite3.connect("db.sqlite3") as conn:
            c = conn.cursor()
            q = f"UPDATE kintai SET created_at='{created_at}', start_or_end='{start_or_end}' WHERE record_id={record_id}"
            print(q)
            c.execute(q)
            conn.commit()

        return q


if __name__ == "__main__":

    database = DataBase(db="db.sqlite3")

    user_id = 1234
    password = "password"
    # ユーザの登録ができるか
    query_user = database.register_user(user_id=user_id, password=password)

    dt_now = datetime.datetime.now()
    str_start = dt_now.strftime("%Y/%m/%d/%H:%M:%S")
    # 出勤の登録ができるか
    query_user = database.register_kintai(
        user_id=user_id, created_at=str_start, start_or_end="start"
    )

    td = datetime.timedelta(hours=7, minutes=30)
    str_end = (dt_now + td).strftime("%Y/%m/%d/%H:%M:%S")
    # 退勤の登録ができるか
    query_user = database.register_kintai(
        user_id=user_id, created_at=str_end, start_or_end="end"
    )

    # ユーザの読み出しができるか
    result = database.load_user(user_id=user_id)
    print(result)

    # 該当ユーザがいない時の結果
    result = database.load_user(user_id="2345")
    print(result)

    # 出退勤の読み出しができるか
    result = database.load_kintai(user_id="1234")
    print(result)

    # 該当ユーザがいない時の結果
    result = database.load_kintai(user_id="2345")
    print(result)

    # パスワードのチェックができるか
    result = database.check_user_password(user_id="1234", password=password)
    print(result)
    result = database.check_user_password(user_id="1234", password="Password")
    print(result)

    # 編集ができるか
    # 該当ユーザがいない時の結果
    result = database.edit_record(record_id=1, created_at=str_end, start_or_end="end")
    print(result)
