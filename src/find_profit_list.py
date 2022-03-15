from typing import List, Dict, Tuple

from functools import reduce
from itertools import permutations, combinations


currency_names = ["RUB", "USD", "EUR", "GBP"]

actual_currs = {
    ("RUB", "USD"): 0.007575757575757576,
    ("RUB", "EUR"): 0.006887052341597796,
    ("RUB", "GBP"): 0.005827505827505828,
    ("USD", "RUB"): 108.0,
    ("USD", "EUR"): 0.9680542110358181,
    ("USD", "GBP"): 0.748502994011976,
    ("EUR", "RUB"): 118.8,
    ("EUR", "USD"): 1.0730000000090132,
    ("EUR", "GBP"): 0.8183306055646481,
    ("GBP", "RUB"): 140.4,
    ("GBP", "USD"): 1.276,
    ("GBP", "EUR"): 1.165,
}


def comp_profit(actual_currs: Dict[Tuple, float], currs: List[str]) -> float:
    """Оценка профита конвертации по заданному списку валют
    Args:
        actual_currs - список актуальных курсов валюь
        currs - последовательность валют
    """
    acc = 1
    for curr_pair in zip(currs, currs[1:]):
        acc *= actual_currs[curr_pair]
    return acc


def find_profit_list(
    actual_currs: Dict[Tuple, float], currency_names: List[str], max_len_seq=4
) -> List[Tuple[List, float]]:
    """Поиск списка валют с профитом >= 1
    Args:
            actual_currs - список актуальных курсов валюь
            currency_names - список названий валют
    Returns:
            (['GBP', 'USD', 'EUR', 'GBP'], 1.010832384027581)
    """
    profit_list = []
    for i in list(range(2, max_len_seq + 1)):
        for curr_comb in permutations(currency_names, i):
            # добавим в конец валюту, с которой начали
            curr_comb = list(curr_comb) + [curr_comb[0]]
            profit = comp_profit(actual_currs, curr_comb)
            if profit >= 1:
                profit_list.append((curr_comb, profit))
            print(curr_comb, profit)
    return profit_list


# res = find_profit_list(actual_currs, currency_names)
# print(f'Best currency seqs: {res}')
