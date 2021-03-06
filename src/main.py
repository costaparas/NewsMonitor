from config import DB_URI
from config import INTERVAL
from database import DBInterface
from datetime import datetime
from monitor import SBSNewsMonitor

import json
import signal
import sys
import time


DB = None  # database interface


def signal_handler(*args, **kwargs):
    """
    Gracefully exit program by closing open resources.

    :param list args: non-keyword arguments
    :param list kwargs: keyword arguments
    """
    if DB:
        DB.close()
    sys.exit(0)


def main():
    """Program entrypoint."""
    global DB
    signal.signal(signal.SIGINT, signal_handler)
    DB = DBInterface(DB_URI)
    monitors = [SBSNewsMonitor(DB)]
    while True:
        print(f'Current time: {datetime.now()}')
        for monitor in monitors:
            print(json.dumps(monitor.update(), indent=4))
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
