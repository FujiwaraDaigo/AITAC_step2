import sqlite3


def user_password_check(userID, password):
    check_ok = False
    if (userID == "Daigo" and password == "Fujiwara") or (
        userID == "Kempee" and password == "Tahara"
    ):
        check_ok = True

    return check_ok
