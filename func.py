from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from random import choice, choices, shuffle


def generate_password(length: int, choose: list) -> str:
    length = int(length)
    symbols = ''
    password = []
    kirill_up = ''.join(chr(i) for i in range(ord('А'), ord('Я') + 1))
    kirill_low = ''.join(chr(i) for i in range(ord('а'), ord('я') + 1))

    symbols_dict = {"kiril_low": kirill_low,
                    "kiril_up": kirill_up,
                    "latin_low": ascii_lowercase,
                    "latin_up": ascii_uppercase,
                    "digits": digits,
                    "special": punctuation}

    for symbols_set in choose:
        if symbols_set:
            password.append(choice(symbols_dict[symbols_set]))
            symbols += symbols_dict[symbols_set]

    password.extend(choices(symbols, k=length - len(password)))
    shuffle(password)
    res_password = ''.join(password)
    return res_password





