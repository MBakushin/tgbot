import os
import re
import requests
import json
from dotenv import load_dotenv


class ConverterError(Exception):
    pass


class ExchangeRates:
    """Main class for telegram bot with the following possibilities:
       1. To convert one currency into second currency.
    """
    @staticmethod
    def convert(quote, base, amount):
        load_dotenv()
        headers = {"apikey": os.getenv("API_KEY")}
        url = f"https://api.apilayer.com/exchangerates_data/convert?" \
              f"to={quote.upper()}&from={base.upper()}&amount={float(amount)}"
        payload = {}
        try:
            response = requests.request("GET", url, headers=headers,
                                        data=payload)
            if not re.match(r"2\d{2}", str(response.status_code)):
                raise requests.ConnectionError
        except requests.ConnectionError:
            return False
        else:
            price = json.loads(response.content)["result"]
            return f"{amount} {base.upper()} в {quote.upper()} = {price}"
