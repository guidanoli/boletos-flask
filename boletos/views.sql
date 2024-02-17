CREATE VIEW services_statistics AS
SELECT id, name, last_payment_ts
FROM service
LEFT OUTER JOIN (SELECT service_id, MAX(payment_ts) as last_payment_ts
                 FROM boleto
                 GROUP BY service_id)
ON id = service_id
ORDER BY last_payment_ts
