from database import DBInterface
from datetime import datetime
from monitor import NewsMonitor

import json
import signal
import sys
import time


DB_URI = 'sqlite:///news.db'  # database location
DB = None  # database interface
INTERVAL = 5 * 60  # update interval in seconds


def signal_handler(*args):
    """
    Gracefully exit program by closing open resources.

    :param type args: arguments
    """
    if DB:
        DB.close()
    sys.exit(0)


def main():
    """Program entrypoint."""
    global DB
    signal.signal(signal.SIGINT, signal_handler)
    DB = DBInterface(DB_URI)
    monitor = NewsMonitor(DB)
    while True:
        print(f'Current time: {datetime.now()}')
        print(json.dumps(monitor.update(), indent=4))
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
