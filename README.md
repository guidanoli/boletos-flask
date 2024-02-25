# Boleto Manager using Flask

"Boleto" is a common billing system used in Brazil.
This project aims to organize boletos and their payments.

## Dependencies

- Python 3.11 with `sqlite3` built-in

## Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
flask init-db
```

## Run server in debug mode

```sh
flask run --debug
```
