#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	calc_income
# CreatedDate:  2018-06-02 13:44:24 +0900
# LastModified: 2018-06-04 12:02:47 +0900
#


import os
import sys
import numpy as np
import pandas as pd
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime

# myfunc
from working import Working


def main():
    # variable
    data_path = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'jobs.csv')
    keyword = pd.read_csv(data_path, header=None)

    # Setup the Calendar API
    store = file.Storage('credentials.json')
    creds = store.get()
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Call the Calendar API
    Min = datetime(2018, 5, 11).isoformat() + 'Z'
    Max = datetime(2018, 6, 10).isoformat() + 'Z'

    events_result = service.events().list(calendarId='primary', timeMin=Min,
                                          timeMax=Max, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    Data = pd.DataFrame(events)

    working = Working(Data)

    for i in range(len(keyword.columns)):
        working.get_working(keyword.iloc[0, i], keyword.iloc[1, i])


if __name__ == "__main__":
    main()
