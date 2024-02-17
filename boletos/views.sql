CREATE VIEW now AS
SELECT cast(strftime("%s", CURRENT_TIMESTAMP) as int);

CREATE VIEW services_statistics AS
SELECT id, name, last_payment_ts, first_expiry_ts
FROM service
LEFT OUTER JOIN (SELECT service_id AS id1, MAX(payment_ts) as last_payment_ts
                 FROM boleto
                 GROUP BY service_id) ON id = id1
LEFT OUTER JOIN (SELECT service_id AS id2, MIN(expiry_ts) as first_expiry_ts
                 FROM boleto
                 WHERE payment_ts IS NULL
                 AND expiry_ts >= now
                 GROUP BY service_id) ON id = id2
ORDER BY last_payment_ts;