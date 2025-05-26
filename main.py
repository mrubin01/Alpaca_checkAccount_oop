import sys
from datetime import datetime
import config
import yfinance as yf
import alpaca_trade_api as tradeapi
import warnings
import pandas as pd
import Asset
warnings.simplefilter("ignore")

# Instantiate REST API Connection
api_live = tradeapi.REST(key_id=config.API_KEY_LIVE, secret_key=config.SECRET_KEY_LIVE,
                         base_url=config.URL_LIVE, api_version='v2')

# a list with a dict for each symbol
positions = api_live.list_positions()
positions_equities = []
positions_cryptos = []
positions_options = []

for p in positions:
    if p.asset_class == "us_equity":
        positions_equities.append(p.symbol)
    elif p.asset_class == "crypto":
        positions_cryptos.append(p.symbol)
    elif p.asset_class == "us_option":
        positions_options.append(p.symbol)
    else:
        continue

# Cash deposits since Dec-23: this does not factor withdrawals in
TOTAL_DEPOSIT = 0
activities = api_live.get_activities(activity_types="CSD")
activities_df = pd.DataFrame([activity._raw for activity in activities])  # Turn it into a dataframe
deposits = activities_df["net_amount"]
for d in deposits:  # .sum() does not work
    TOTAL_DEPOSIT += float(d)


# equity variables
equity_list = []  # list of equity instances
ticker_tuple = ()
total_value_plus_net_div = 0
winners_and_losers = []
winners = []
losers = []
avg_increase_winners_losers = []
avg_increase_winners = []
avg_increase_losers = []

# crypto variables
crypto_list = []  # list of crypto instances
crypto_tickers = []
crypto_value_at_purchase = 0
crypto_current_value = 0

# Instantiate the equities
for p in positions:
    if p.asset_class == "us_equity":
        ticker_tuple = (p.symbol,
                        p.exchange,
                        p.current_price,
                        p.avg_entry_price,
                        p.qty,
                        p.asset_class
                        )
        # instantiation
        equity = Asset.Equity(str(ticker_tuple[0]),
                              str(ticker_tuple[1]),
                              float(ticker_tuple[2]),
                              float(ticker_tuple[3]),
                              float(ticker_tuple[4]),
                              str(ticker_tuple[5]),
                              float(config.dividend_ytd_dict[p.symbol]),
                              float(config.dividend_full_year_dict[p.symbol]))

        equity_list.append(equity)
        # print(equity_list[-1].get_increase_perc())
        if equity_list[-1].get_increase_perc() is not None:
            winners_and_losers.append(equity_list[-1].symbol)
            avg_increase_winners_losers.append(equity_list[-1].get_increase_perc())
            if equity_list[-1].get_increase_perc() > 0:
                winners.append(equity_list[-1].symbol)
                avg_increase_winners.append(equity_list[-1].get_increase_perc())
            else:
                losers.append(equity_list[-1].symbol)
                avg_increase_losers.append(equity_list[-1].get_increase_perc())
        else:
            pass
        total_value_plus_net_div += equity_list[-1].get_current_value_plus_div()

    else:
        ticker_tuple = (p.symbol,
                        p.exchange,
                        p.current_price,
                        p.avg_entry_price,
                        p.qty,
                        p.asset_class
                        )
        # instantiation
        crypto = Asset.Crypto(str(ticker_tuple[0]),
                              str(ticker_tuple[1]),
                              float(ticker_tuple[2]),
                              float(ticker_tuple[3]),
                              float(ticker_tuple[4]),
                              str(ticker_tuple[5]))

        crypto_list.append(crypto)
        crypto_tickers.append(str(ticker_tuple[0]))
        crypto_value_at_purchase += crypto_list[-1].get_value_at_purchase()
        crypto_current_value += crypto_list[-1].get_current_value()


def main():
    print("\n" + "+++++ WINNERS +++++")
    print(winners)
    print("Avg Increase Winners: " + str(round(sum(avg_increase_winners) / len(winners), 3)) + "%")
    print()
    print("+++++ LOSERS +++++")
    print(losers)
    print("Avg Decrease Losers: " + str(round(sum(avg_increase_losers) / len(losers), 3)) + "%")
    print()
    print("+++++ OVERALL AVG INCREASE (PRICE + (DIVIDENDS - WITHHOLDING TAX 15%)) +++++")
    print(str(round(sum(avg_increase_winners_losers) / len(winners_and_losers), 3)) + "%")
    print()
    print("Total Amount deposited: " + str(round(TOTAL_DEPOSIT, 3)))
    print("Total Value including net dividends: " + str(round(total_value_plus_net_div, 3)))
    print()
    print("+++++ CRYPTOS +++++")
    print(crypto_tickers)
    print("Value at purchase: " + str(round(crypto_value_at_purchase, 3)))
    print("Current value: " + str(round(crypto_current_value, 3)))
    print()
    print("+++++ MONTHLY DIVIDENDS +++++")
    for key, value in config.monthly_net_dividends.items():
        print(key, value)
    print()
    print("Total dividends YTD " + str(sum(config.monthly_net_dividends.values())))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
