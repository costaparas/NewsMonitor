FROM python:3.8.8-alpine

LABEL project="News Monitor"
LABEL maintainer="Costa Paraskevopoulos"

# install dependencies
RUN apk add build-base
RUN apk add --no-cache \
    gcc \
    # local project directory
    && mkdir /NewsMonitor

# add requirements file
COPY requirements.txt /tmp/requirements.txt

# install python dependencies
RUN pip install -U pip \
    && pip install -r /tmp/requirements.txt

# copy sources
COPY . /NewsMonitor

# project entrypoint
WORKDIR /NewsMonitor/src
ENTRYPOINT ["python"]
CMD ["main.py"]
