# NewsMonitor
A general-purpose news website scraper and change monitor

## Description

A specific news website is monitored at a regular interval and changes in tracked items are detected and reported to standard output in a JSON format.

Currently, there are 3 types of changes detected/reported:
- A new item is added to the page.
- A previously-detected item is removed from the page.
- A previously-detected item is updated in some way.

The system could easily be extended to also track changes such as the order of items on the page.

Currently, the [SBS News website](https://www.sbs.com.au/news/) is monitored and 3 types of items are tracked for changes:
- Section headings
- Article/article previews
- Menu items/menu links

The system could easily be extended to also track changes to the elements on the page that are of interest, though would likely change less frequently.

### Multi-Website Monitoring

The system is designed to make is possible to monitor multiple news sources, and is not specific to SBS sites.

News monitoring is achieved by defining the relevant URL, item selector and metadata selectors in a subclass of the abstract base class `NewsMonitor` defined in [`monitor.py`](src/monitor.py). The abstract base class defines the necessary methods for detecting and reporting the updates - they need not be implemented in the base class.

If more news websites are to be monitored, an appropriate base class should be defined with the desired fields, and a corresponding object ought to be created and added to the `monitors` list in [`main.py`](src/main.py).

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

# Run program ad-hoc
python src/main.py

# Run unit tests
rm test.db
pytest -sv tests/*

# Check unit testing coverage
rm test.db
coverage run -m pytest tests/*
coverage report -m src/*.py tests/*.py
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

### Configuration

Some configuration settings are defined in config.py. In particular:
- `DB_URI`: location of the main program database
- `TEST_DB_URI`: location of the database to use for testing
- `INTERVAL`: the update frequency (in seconds)

Currently, the update interval is set to 5 minutes, but can be changed to something more suitable as needed.

## License
Copyright (C) 2021 Costa Paraskevopoulos

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see http://www.gnu.org/licenses/.
