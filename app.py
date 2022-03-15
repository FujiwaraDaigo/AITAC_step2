from flask import Flask, redirect, render_template, request
import dataframe_io
import data_processor
import user_checker
import uuid
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


class User(UserMixin):
    def __init__(self, uid):
        self.id = uid


# Cookieを持ってない人はログインページに強制的にリダイレクト
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect("/login")


@app.route("/login")
def login():
    user = User(uuid.uuid4())  # ランダムなIDを発行する
    login_user(user)  # ログイン
    return render_template("login_form.html")


@login_manager.user_loader
def load_user(uid):
    return User(uid)


@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    return redirect("/login")


@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    session = current_user.id
    userID = request.form.get("userID")
    password = request.form.get("password")
    check_ok = user_checker.user_password_check(userID, password)
    if check_ok:
        return render_template(
            "home.html", title="home", session=session, userID=userID
        )
    else:
        return render_template("login_failure.html")


@app.route("/stock_page", methods=["GET"])
@login_required
def stock_form():
    return render_template("stock.html")


@app.route("/stock_register", methods=["POST"])
@login_required
def register_stock():
    portfolio_id = request.form.get("portfolio_id")
    code = request.form.get("code")
    name = request.form.get("name")

    df = dataframe_io.register_stock_data(code=code, name=name)
    df = dataframe_io.load_stok_data(name=name)
    image_path = data_processor.plot_price_transition(df, name)
    dataframe_io.register_portfolio(
        portfolio_id=portfolio_id, stock_name=name, image_path=image_path
    )
    # image_path2 = data_processor.plot_candle(df)

    return render_template("stock.html")


@app.route("/stock_review", methods=["POST"])
@login_required
def stock_review():
    portfolio_id = request.form.get("portfolio_id2")
    portfolio = dataframe_io.load_portfolio(portfolio_id=portfolio_id)

    print(portfolio)

    return render_template("stock_review.html", portfolio=portfolio)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
