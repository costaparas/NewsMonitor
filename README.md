# NewsMonitor
A general-purpose news website scraper and change monitor

## Description

TODO

## Getting Started

### Local Development

It is assumed that:
* Python version 3.8.8 or above is installed (<https://www.python.org/downloads/>)

```sh
# Create a virtual environment
python -m venv env

# Enter the virtual environment
source env/bin/activate

# Install requirements
pip install -r requirements.txt

# Run program
python src/main.py

# Run tests
rm test.db
pytest -sv tests/*
```

### Using Docker

It is assumed that:
* Docker version 19.03.6 or above is installed (<https://docs.docker.com/get-docker/>)

```sh
# Build docker image from the Dockerfile
docker build -t news-monitor:1.0 .

# Run container based on the built image
docker run news-monitor:1.0

# Delete the docker image
docker rmi news-monitor:1.0 -f
```

## License
Copyright (C) 2021 Costa Paraskevopoulos

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
