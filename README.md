# Boleto Manager using Flask

"Boleto" is a common billing system used in Brazil.
This project aims to organize boletos and their payments.

## Entity-relationship model

Attributes are typed as `sqlite3` storage classes.

```mermaid
erDiagram
    
    SERVICE {
        INTEGER id PK
        INTEGER active
        TEXT frequency
        TEXT name
    }
    
    BOLETO {
        INTEGER id PK
        INTEGER issue_ts
        INTEGER expiry_ts
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
        INTEGER ts
    }
    
    PERSON {
        INTEGER id PK
        TEXT name
    }

    REIMBURSEMENT {
        INTEGER boleto_id PK, FK
        INTEGER from_id PK, FK
        INTEGER to_id PK, FK
    }

    SERVICE ||--o{ BOLETO : issues
    BOLETO ||--o{ CHARGE : inflicts
    CHARGE }o--|| PERSON : "is meant for"
    PERSON ||--o{ PAYMENT : makes
    PAYMENT |o--|| BOLETO : covers
```
