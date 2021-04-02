from config import DB_URI
from config import INTERVAL
from database import DBInterface
from datetime import datetime
from monitor import NewsMonitor

import json
import signal
import sys
import time


DB = None  # database interface


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
