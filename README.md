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
        TEXT name
        TEXT freq
        INTEGER active
    }
    
    BOLETO {
        INTEGER id PK
        INTEGER issue_ts
        INTEGER expiry_ts
        BLOB file
    }

    PERSON {
        INTEGER id PK
        TEXT name
    }

    CHARGE {
        INTEGER boleto_id PK, FK
        INTEGER person_id PK, FK
        INTEGER amount
    }

    PAYMENT {
        INTEGER boleto_id PK, FK
        INTEGER person_id PK, FK
        INTEGER amount
        INTEGER ts
    }

    SERVICE ||--o{ BOLETO : issues
    BOLETO ||--o{ CHARGE : inflicts
    CHARGE }o--|| PERSON : on
    PERSON ||--o{ PAYMENT : makes
    PAYMENT }o--|| BOLETO : covers
```
