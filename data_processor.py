import matplotlib

matplotlib.use("Agg")
import mplfinance as mpf
from matplotlib.dates import DateFormatter, DayLocator, MonthLocator, AutoDateLocator
from matplotlib import pyplot as plt
import os


def plot_price_transition(df, name: str):
    # 最高値と最低値の平均
    means = (df["High"] + df["Low"]) / 2
    times = df.index

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(times, means)
    # ax.xaxis.set_major_locator(MonthLocator(interval=12))
    ax.xaxis.set_major_locator(AutoDateLocator(minticks=5, maxticks=12))
    ax.xaxis.set_major_formatter(DateFormatter("%Y\n%m/%d"))
    ax.set_xlim(times[0], times[-1])
    ax.set_title(name)
    ax.set_xlabel("price")
    ax.set_ylabel("time")
    ax.legend()

    # 最高値と最低値の間を塗りつぶす
    plt.fill_between(times, df["High"], df["Low"], alpha=0.2)

    image_path = "./static/figure/kintai_transition_" + name + ".png"
    fig.savefig(image_path)
    return image_path


# ローソク足チャート(期間が短いとき限定)
def plot_candle(df):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    image_path = "./static/figure/candlestick_mpf_candle.png"
    mpf.plot(
        df,
        type="candle",
        figratio=(12, 4),
        savefig=image_path,
    )
    return image_path
