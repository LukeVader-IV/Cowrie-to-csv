# Cowrie CSV server
Host a web server with a CSV containing basic information collected by cowrie.<br>
This allows basic information to be fetched from a different instance, and ingested e.g. by MISP.

## Installation

1. clone this repository
2. In the repo's directory, run `docker build . -t cowrie-to-csv`
3. In the docker compose file, modify the port if desired.
4. `docker compose up -d`
5. Access the csv ( default at http://localhost:8000 )

## Help

- How do i make this tool use HTTPS ?

Place it behind a reverse proxy (NGINX)

- Why can't i access it from outside the machine/network

Ensure that the docker compose ports and the env `PORT` are equal.
Check that there is no firewall in the way.