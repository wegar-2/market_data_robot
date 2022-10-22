import os
from market_data_robot.stooq.stooq_fetcher import StooqFetcher
from market_data_robot.email_sender.email_sender import SslGmailSender
import datetime as dt

# prepare fetching parameters
date_today = dt.date.today()
date_end = date_today + dt.timedelta(days=-1)
date_start = date_today.replace(year=date_today.year - 1)
str_ticker = "BTC.V"

# load the data from stooq & make a figure
sf = StooqFetcher()
df = sf.df_get_daily_data_for_ticker_for_dates_range(str_ticker=str_ticker, date_start=date_start, date_end=date_end)
fig = sf.make_plot_of_close_prices(df=df, str_ticker=str_ticker)
fig.show()
fig.savefig("myfig.png")

# send email with CSV
sender = SslGmailSender(
    str_sender_email=os.getenv("MARKET_DATA_ROBOT_GMAIL_USERNAME"),
    str_password=os.getenv("MARKET_DATA_ROBOT_GMAIL_PASSWORD")
)
sender.send_email_with_csv_and_fig_attachment(
    str_email_text="Find data attached",
    str_receiver="awegrzyn17@gmail.com",
    str_subject=f"Time series data from Stooq for ticker {str_ticker} for last 1Y",
    df=df,
    fig=fig
)
