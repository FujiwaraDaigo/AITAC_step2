from flask import Flask, redirect, render_template, request

# MySQLを使う場合
from database_MySQL import DataBase

# sqlite3を使う場合
# from database import DataBase
import os

from flask_login import (
    LoginManager,
    UserMixin,
    login_required,
    login_user,
    logout_user,
    current_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
login_manager = LoginManager()
login_manager.init_app(app)
database = DataBase(db="db.sqlite3")

### ログイン機能###############################################
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    # def get(self, uid):
    #     return self.id


# Cookieを持ってない人はログインページに強制的にリダイレクト
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect("/login_form")


@login_manager.user_loader
def load_user(user_id):
    return User(user_id=user_id)


###↑↑↑######################################################


@app.route("/login_form")
def login_form():
    return render_template("login_form.html")


@app.route("/signup", methods=["GET"])
def signup():
    logout_user()
    return render_template("signup.html")


@app.route("/login_check", methods=["POST"])
def login_check():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    check_ok = database.check_user_password(user_id=user_id, password=password)
    if check_ok == 1:
        user = User(user_id=user_id)  # ランダムなIDを発行する
        login_user(user)  # ログイン
        return redirect("/")
    elif check_ok == -1:
        return render_template("login_failure.html", message="パスワード不一致")
    else:
        return render_template("login_failure.html", message="未登録")


@app.route("/signin", methods=["POST"])
def signin():
    user_id = request.form.get("user_id")
    password = request.form.get("password")
    database.register_user(user_id=user_id, password=password)
    return redirect("/login_form")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/login_form")


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    user_id = current_user.id
    return render_template("home.html", title="home", user_id=user_id)


@app.route("/register_kintai", methods=["POST"])
@login_required
def register_kintai():
    start_or_end = request.form.get("start_or_end")
    user_id = current_user.id

    database.register_kintai(
        user_id=user_id, start_or_end=start_or_end, created_at="now"
    )

    return redirect("/kintai_review")


@app.route("/kintai_review", methods=["GET"])
@login_required
def kintai_review():
    user_id = current_user.id
    kintai_info = database.load_kintai(user_id=user_id)

    return render_template(
        "kintai_review.html", user_id=user_id, kintai_info=kintai_info, record_id=-1
    )


@app.route("/remove", methods=["POST"])
@login_required
def remove():
    user_id = current_user.id
    record_id = request.form.get("record_id")
    database.remove_record(record_id=record_id)
    kintai_info = database.load_kintai(user_id=user_id)

    return render_template(
        "kintai_review.html", user_id=user_id, kintai_info=kintai_info, record_id=-1
    )


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    user_id = current_user.id
    record_id = request.form.get("record_id")
    kintai_info = database.load_kintai(user_id=user_id)

    return render_template(
        "kintai_review.html",
        user_id=user_id,
        kintai_info=kintai_info,
        record_id=record_id,
    )


@app.route("/execute_edit", methods=["POST"])
@login_required
def execute_edit():
    user_id = current_user.id
    record_id = request.form.get("record_id")
    created_at = request.form.get("created_at")
    start_or_end = request.form.get("start_or_end")
    database.edit_record(
        record_id=record_id, created_at=created_at, start_or_end=start_or_end
    )
    kintai_info = database.load_kintai(user_id=user_id)

    return render_template(
        "kintai_review.html",
        user_id=user_id,
        kintai_info=kintai_info,
        record_id=-1,
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
