DROP TABLE IF EXISTS service;
DROP TABLE IF EXISTS boleto;

CREATE TABLE service (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR UNIQUE NOT NULL,
    frequency VARCHAR NOT NULL
);

CREATE TABLE boleto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_id INTEGER NOT NULL REFERENCES service(id),
    filename VARCHAR NOT NULL,
    amount REAL NOT NULL,
    expiry_ts INTEGER NOT NULL,
    paid INTEGER NOT NULL
);
