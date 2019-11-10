# www.bareasgi.com

## Building

```bash
poetry install
```

## Installation

```bash
sudo cp etc/bareasgi-web-server.service /lib/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable bareasgi-web-server
sudo systemctl start bareasgi-web-server
```
