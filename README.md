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
```

## Entity-relationship model

Attributes are typed as `sqlite3` storage classes.

```mermaid
erDiagram

    SERVICE {
        INTEGER id PK
        VARCHAR name "NOT NULL"
    }
    
    BOLETO {
        INTEGER id PK
        INTEGER service_id FK "NOT NULL"
        VARCHAR filename "NOT NULL"
        REAL amount "NOT NULL"
        INTEGER issue_ts "NOT NULL"
        INTEGER expiry_ts "NOT NULL"
        INTEGER payment_ts
    }

    SERVICE ||--o{ BOLETO : issues
```
