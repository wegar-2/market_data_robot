import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")


class StooqFetcher:

    def __init__(self):
        pass

    def df_get_daily_data_for_ticker_for_dates_range(
            self, str_ticker: str, date_start: dt.date, date_end: dt.date) -> pd.DataFrame:
        # 1. concatenate the URL
        str_url = f"https://stooq.com/q/d/l/?s={str_ticker}&d1={date_start.strftime('%Y%m%d')}" \
                  f"&d2={date_end.strftime('%Y%m%d')}&i=d"
        df = pd.read_csv(str_url)
        df = df[["Date", "Close"]].copy()
        df["Date"] = [pd.to_datetime(dt.datetime.strptime(el, '%Y-%m-%d')) for el in df["Date"]]
        df.rename(columns={"Date": "quote_date", "Close": "close_" + str_ticker}, inplace=True)
        return df

    @staticmethod
    def make_plot_of_close_prices(df: pd.DataFrame, str_ticker: str):
        fig = plt.figure()
        plt.plot(df["quote_date"], df["close_BTC.V"], figure=fig)
        plt.xlabel("quote dates", figure=fig)
        plt.ylabel("price", figure=fig)
        plt.title("Time Series of Prices for Ticker " + str_ticker + " Based on Stooq Data", figure=fig)
        return fig

