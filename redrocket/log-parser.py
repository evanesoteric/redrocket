#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
    Checks log every 8 minutes to ensure video are being watched. Otherwise it kills the bot and waits for stat cronjob.
'''

import subprocess
from datetime import datetime, timedelta

from config import *

TIME_DELTA = 8
TIMESTAMP_REGEX = re.compile("\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}")


def filter_logs(log_file):
    max_time = datetime.now() - timedelta(minutes=TIME_DELTA)

    # reserve log file to process the last line first
    for line in reversed(list(open(log_file))):
        line = line.strip()
        if not line or "current video:" not in line:
            continue

        # parse time stamp of log
        entry_timestamp_match = TIMESTAMP_REGEX.search(line)
        if not entry_timestamp_match:
            continue

        entry_timestamp = datetime.strptime(entry_timestamp_match.group(), "%Y-%m-%d %H:%M")

        # if entry timestamp older than previous 15 munites than return (No occur)
        if entry_timestamp < max_time:
            logging.critical('log-parser - current track occurrence not found within 8 minutes. Killing bot!')

            # kill bot, wait for bot-stat
            subprocess.run(['bash', homedir + '/kill.sh'])
            time.sleep(3)

        # event occur, print the line of log
        # print(line)
        return



if __name__ == "__main__":
    log_file_path = str(homedir) + '/bot.log'
    # log_file_path = 'bot.log'
    if not os.path.isfile(log_file_path):
        # print('Log file not found: {}'.format(log_file_path))
        logging.critical('log-parser - log file not found!')
        # sentry.capture_message(hostname + ': URGENT: log-parser - log file not found!')
    else:
        filter_logs(log_file_path)

    sys.exit()
