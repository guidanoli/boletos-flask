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

## Run server

```sh
flask run
```

## Configure system to always run server in debug mode on startup

Here's a step-by-step guide for configuring your system to run the server on startup.
Superuser privileges might be necessary to run some commands.

1. Create the following file under `/etc/systemd/system/boletos.service`.
You can replace `USERNAME` with your username,
and `REPOSITORY-PATH` with the path to the copy of this repository on your local machine.

```service
[Unit]
Description=Manage the payment of boletos with an easy-to-use web interface!
After=network.target

[Service]
User=<USERNAME>
WorkingDirectory=<REPOSITORY-PATH>
ExecStart=<REPOSITORY-PATH>/.venv/bin/flask run
Restart=always

[Install]
WantedBy=multi-user.target
```

2. Change the mode of this file to 644.

```sh
chmod 644 /etc/systemd/system/boletos.service
```

3. Start the service.

```sh
systemctl start boletos
```

4. Check the status of the service.

```sh
systemctl status boletos
```

5. Enable the service (to run on startup).

```sh
systemctl enable boletos
```
