import requests
import json
from nbv import *

class ApiExeption(Exception):
    pass

class Converter :
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base.lower()]
        except KeyError:
            raise ApiExeption(f'Валюта {base} не найдена')

        try:
            quote_key = keys[quote.lower()]
        except KeyError:
            raise ApiExeption(f'Валюта {quote} не найдена')

        if base_key == quote_key:
            raise ApiExeption(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise ApiExeption(f'Не удалось обработать количество{amount}!')


        response_USD = requests.get(f"https://api.apilayer.com/exchangerates_data/convert?to="
                                    f"{base_key}&from={quote_key}&amount={amount}",
                                    headers=headers)
        res_USD = json.loads(response_USD.content)
        new_price_USD = res_USD['info']['rate']
        new_amount = res_USD['query']['amount']
        price_ = float(new_amount) * float(new_price_USD)
        priсe = round((price_), 2)
        return priсe
