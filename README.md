# Boleto Manager using Flask

"Boleto" is a common billing system used in Brazil.
This project aims to organize boletos and their payments.

## Entity-relationship model

Attributes are typed as `sqlite3` storage classes.

```mermaid
erDiagram
    
    SERVICE {
        INTEGER id PK
        TEXT name
    }
    
    BOLETO {
        INTEGER id PK
        INTEGER due_date_ts
        BLOB file
    }

    CHARGE {
        INTEGER boleto_id PK, FK
        INTEGER person_id PK, FK
        REAL amount
    }

    PAYMENT {
        INTEGER boleto_id PK, FK
        INTEGER person_id PK, FK
        INTEGER payment_date_ts
    }
    
    PERSON {
        INTEGER id PK
        TEXT name
    }

    SERVICE ||--o{ BOLETO : issues
    BOLETO }o--|{ CHARGE : inflicts
    CHARGE }o--|{ PERSON : "is meant for"
    PERSON |o--o{ PAYMENT : makes
    PAYMENT |o--o{ BOLETO : covers
```
