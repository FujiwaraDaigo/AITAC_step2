import investpy
import sqlite3
import pandas as pd

from matplotlib.dates import date2num


def register_stock_data(
    code: str, name: str, country="japan", from_date="28/07/2011", to_date="28/07/2021"
):

    with sqlite3.connect("db.sqlite3") as conn:

        stock_data = investpy.get_stock_historical_data(
            stock=code, country=country, from_date=from_date, to_date=to_date
        )
        stock_data.to_sql("stock_data_" + name, conn, if_exists="replace", index=True)

    return stock_data


def load_stok_data(name: str):
    """[summary]

    Parameters
    ----------
    name : str
        [description]

    Returns
    -------
    [type]
        [description]
    """
    table_name = "stock_data_" + name

    with sqlite3.connect("db.sqlite3") as conn:
        query = "SELECT * FROM " + table_name
        df = pd.read_sql_query(query, conn, index_col="Date", parse_dates="Date")

    return df


def register_portfolio(portfolio_id: int, stock_name: str, image_path: str):
    """ポートフォリオテーブルにidと銘柄名と銘柄の画像パスを登録

    Parameters
    ----------
    portfolio_id : int
        [description]
    name : str
        [description]
    image_path : str
        [description]
    """
    with sqlite3.connect("db.sqlite3") as con:
        c = con.cursor()
        q = f"""
                        insert into portfolio(portfolio_id, stock_name, image_path) values(
                            {portfolio_id}, '{stock_name}', '{image_path}' 
                        )
                    """
        print(q)
        c.execute(q)
        con.commit()


def load_portfolio(portfolio_id: int):
    with sqlite3.connect("db.sqlite3") as con:
        c = con.cursor()
        q = f"""
                    select * from portfolio
                    where portfolio_id = {portfolio_id} 
                    order by stock_name asc
                """
        c.execute(q)
        portfolio_list = c.fetchall()

    return portfolio_list


if __name__ == "__main__":

    code = "7203"  # トヨタ自動車
    name = "toyota"

    # データの登録ができるか
    stock_data = register_stock_data(code=code, name=name)
    print("registered")
    print(stock_data.head())
    print("")

    # データの読み出しができるか
    df = load_stok_data(name=name)
    print("loaded")
    print(stock_data.head())
    print("")
