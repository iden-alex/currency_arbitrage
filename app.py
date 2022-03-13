from multiprocessing import Barrier
import random
import time
import requests

from itertools import permutations


class BadResponse(Exception):
    pass


CURRENCIES = ["RUB", "USD", "EUR", "GBP"]
all_permutations = list(permutations(CURRENCIES, 2))

HEADERS = {
    "Accept": "*/*",
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (X11; Linux i686 on x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67\
         Safari/537.36 OPR/56.0.3051.104",
}


def find_pair(rates, from_currency, to_currency) -> float:
    for rate in rates:
        if (
            rate["fromCurrency"]["name"] == from_currency
            and rate["toCurrency"]["name"] == to_currency
        ):
            return rate["buy"]
        if (
            rate["fromCurrency"]["name"] == to_currency
            and rate["toCurrency"]["name"] == from_currency
        ):
            return 1 / rate["sell"]


def get_current_currency() -> dict:
    response = requests.get(
        "https://api.tinkoff.ru/v1/currency_rates", timeout=10, headers=HEADERS
    )
    if response.status_code != 200:
        raise BadResponse
    res = {}
    for pair in all_permutations:
        res[pair] = find_pair(response.json()["payload"]["rates"], *pair)
    return res


def sleep():
    random.seed(time.time())
    time_for_sleep = 300 + random.randint(1, 30)
    time.sleep(time_for_sleep)
