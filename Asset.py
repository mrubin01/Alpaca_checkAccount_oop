# A Parent Class can be declared just with class Asset rather than class Asset(object):

import config


class Asset(object):
    def __init__(self, symbol, exchange, current_price):
        self.symbol = symbol
        self.exchange = exchange
        self.current_price = current_price

    def __str__(self):
        return f"{self.symbol} is an asset listed in {self.exchange}"

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, new_symbol):
        if isinstance(new_symbol, str):
            self._symbol = new_symbol
        else:
            print("Invalid symbol! It must be a string")

    @property
    def exchange(self):
        return self._exchange

    @exchange.setter
    def exchange(self, new_exchange):
        if isinstance(new_exchange, str):
            self._exchange = new_exchange
        else:
            print("Invalid exchange! It must be a string")

    @property
    def current_price(self):
        return self._current_price

    @current_price.setter
    def current_price(self, new_current_price):
        if isinstance(new_current_price, float) and new_current_price > 0:
            self._current_price = new_current_price
        else:
            print("Invalid price! It must be a float")

    def print_asset_detail(self):
        print(f"Info about: {self._symbol}")
        print(f"Exchange {self._exchange}" + "\n")


class Equity(Asset):

    def __init__(self, symbol, exchange, current_price, avg_entry_price, qty, asset_class, div_ytd, div_full_year):
        super(Equity, self).__init__(symbol, exchange, current_price)

        self.avg_entry_price = avg_entry_price
        self.qty = qty
        self.asset_class = asset_class
        self.div_ytd = div_ytd
        self.div_full_year = div_full_year

    def __str__(self):
        return f"Equity {self.symbol} current price is {self.current_price}: you have {self.qty} shares \n"

    @property
    def avg_entry_price(self):
        return self._avg_entry_price

    @avg_entry_price.setter
    def avg_entry_price(self, new_avg_entry_price):
        if isinstance(new_avg_entry_price, float):
            self._avg_entry_price = new_avg_entry_price
        else:
            print("Invalid avg entry price! It must be a float")

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, new_qty):
        if isinstance(new_qty, float) or isinstance(new_qty, int):
            self._qty = new_qty
        else:
            print("Invalid qty! It must be a float or an integer!")

    @property
    def asset_class(self):
        return self._asset_class

    @asset_class.setter
    def asset_class(self, new_asset_class):
        if isinstance(new_asset_class, str):
            self._asset_class = new_asset_class
        else:
            print("Invalid asset class! It must be a string")

    @property
    def div_ytd(self):
        return self._div_ytd

    @div_ytd.setter
    def div_ytd(self, new_div_ytd):
        if isinstance(new_div_ytd, float) and new_div_ytd >= 0:
            self._div_ytd = new_div_ytd

        else:
            print("Invalid dividend YTD! It must be a float")

    @property
    def div_full_year(self):
        return self._div_full_year

    @div_full_year.setter
    def div_full_year(self, new_div_full_year):
        if isinstance(new_div_full_year, float) and new_div_full_year >= 0:
            self._div_full_year = new_div_full_year
        else:
            print("Invalid dividend Full Year! It must be a float")

    def get_net_dividend(self):
        # subtract the 15% withholding tax from the dividends
        return [round(self._div_ytd * 0.85, 3), round(self._div_full_year * 0.85, 3)]

    def get_div_yield(self):
        if self._current_price != 0:
            net_yield_ytd = (self.get_net_dividend()[0] / self._current_price) * 100
            net_yield_full_year = (self.get_net_dividend()[1] / self._current_price) * 100
            return [round(net_yield_ytd, 3), round(net_yield_full_year, 3)]
        else:
            net_yield_ytd = 0
            net_yield_full_year = 0
            return [net_yield_ytd, net_yield_full_year]

    def get_current_price_plus_net_dividend_ytd(self):
        return round(self._current_price + (self._div_ytd * 0.85), 3)

    def get_value_at_purchase(self):
        return round(self._avg_entry_price * self._qty, 3)

    def get_current_value(self):
        return round(self._current_price * self._qty, 3)

    # def get_current_value_plus_div(self):
    #     return round(self.get_current_price_plus_net_dividend_ytd() * self._qty, 3)

    def get_current_value_plus_div(self):
        return (self._current_price * self._qty) + config.net_dividend_received_ytd_dict[self._symbol]

    def get_increase_perc(self):
        if self.get_value_at_purchase() != 0:
            return round((self.get_current_value_plus_div() - self.get_value_at_purchase()) / self.get_value_at_purchase() * 100, 3)
        else:
            return None


class Crypto(Asset):

    def __init__(self, symbol, exchange, current_price, avg_entry_price, qty, asset_class):
        super(Crypto, self).__init__(symbol, exchange, current_price)

        self.avg_entry_price = avg_entry_price
        self.qty = qty
        self.asset_class = asset_class

    def __str__(self):
        return f"Crypto {self.symbol} current price is {self.current_price}: you have {self.qty} shares \n"

    @property
    def avg_entry_price(self):
        return self._avg_entry_price

    @avg_entry_price.setter
    def avg_entry_price(self, new_avg_entry_price):
        if isinstance(new_avg_entry_price, float):
            self._avg_entry_price = new_avg_entry_price
        else:
            print("Invalid avg entry price! It must be a float")

    @property
    def qty(self):
        return self._qty

    @qty.setter
    def qty(self, new_qty):
        if isinstance(new_qty, float) or isinstance(new_qty, int):
            self._qty = new_qty
        else:
            print("Invalid qty! It must be a float or an integer!")

    @property
    def asset_class(self):
        return self._asset_class

    @asset_class.setter
    def asset_class(self, new_asset_class):
        if isinstance(new_asset_class, str):
            self._asset_class = new_asset_class
        else:
            print("Invalid asset class! It must be a string")

    def get_value_at_purchase(self):
        return round(self._avg_entry_price * self._qty, 3)

    def get_current_value(self):
        return round(self._current_price * self._qty, 3)

    def get_increase_perc(self):
        if self.get_value_at_purchase() != 0:
            return round((self.get_current_value() - self.get_value_at_purchase()) / self.get_value_at_purchase() * 100, 3)
        else:
            return None

