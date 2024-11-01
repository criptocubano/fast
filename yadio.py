import requests
from pprint import pprint


def make_request(url: str):
    """Función para realizar una solicitud GET y manejar errores."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("Error al realizar la solicitud:", e)
        return None


def get_currencies():
    url = 'https://api.yadio.io/currencies'
    currencies = make_request(url)

    if currencies is not None:
        # Convertir la respuesta JSON en un diccionario con índices
        return {index + 1: currency for index, currency in enumerate(currencies)}
    return None


def convert_currencies(amount: int, currency_from: str, currency_to: str):
    url = f'https://api.yadio.io/convert/{amount}/{currency_from}/{currency_to}'
    return make_request(url)


def rate_currencies(currency_1: str, currency_2: str):
    url = f'https://api.yadio.io/rate/{currency_1}/{currency_2}'
    return make_request(url)


# Ejemplo de uso
if __name__ == "__main__":
    pprint(rate_currencies("CUP", "USD"))
    pprint(get_currencies())
