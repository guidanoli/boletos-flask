DROP TABLE IF EXISTS service;
DROP TABLE IF EXISTS payment;

CREATE TABLE service (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR UNIQUE NOT NULL,
    active INTEGER NOT NULL DEFAULT (1)
);

CREATE TABLE payment (
    service_id INTEGER NOT NULL REFERENCES service(service_id),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    filename VARCHAR NOT NULL,
    PRIMARY KEY (service_id, year, month)
)
