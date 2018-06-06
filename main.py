#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	calc_income
# CreatedDate:  2018-06-02 13:44:24 +0900
# LastModified: 2018-06-06 12:35:25 +0900
#


import os
import sys
import numpy as np
import pandas as pd
import argparse
import re
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime

# myfunc
from working import Working


def main():
    # option
    parser = argparse.ArgumentParser(
        description='calculation income from google calendar')
    parser.add_argument('-m', '--month', metavar='YYYY-MM', action='store',
                        nargs='?', help='choice month', default=datetime.now().strftime("%Y-%m"))
    args = parser.parse_args()

    # variable
    data_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'jobs.csv')
    keyword = pd.read_csv(data_path, header=None)
    year = int(re.sub(r"-.*$", "", args.month))
    month = int(re.sub(r"^.*-", "", args.month))

    # Setup the Calendar API
    store = file.Storage('credentials.json')
    creds = store.get()
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    Min = datetime(year, month, 11).isoformat() + 'Z'
    Max = datetime(year, (month + 1)%12, 10).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=Min,
                                          timeMax=Max, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    Data = pd.DataFrame(events)

    working = Working(Data)

    for i in range(len(keyword.columns)):
        working.get_working(keyword.iloc[0, i], keyword.iloc[1, i])


if __name__ == "__main__":
    main()
