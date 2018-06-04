#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	calc_income
# CreatedDate:  2018-06-02 13:44:24 +0900
# LastModified: 2018-06-04 11:13:27 +0900
#


import os
import sys
import numpy as np
import pandas as pd
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime


def calc_income(tdelta, hour_wage):
    # variable
    working_hours = tdelta.seconds / (60**2)
    break_time = 1
    boundary = 6
    working_max = 8

    if working_hours > boundary:
        working_hours = working_hours - break_time

    if working_hours > working_max:
        working_hours = working_max + (working_hours - working_max) * 1.25

    return hour_wage * working_hours


def get_working(Data, name, hour_wage):
    # variable
    income = 0
    time_format = "%Y-%m-%d %H:%M:%S"

    Data = Data[Data['summary'] == name].reset_index(drop=True)

    for i in range(len(Data.index)):
        start = Data.loc[i, 'start'].get(
            'dateTime', Data.loc[i, 'start'].get('date')).replace("T", " ")
        end = Data.loc[i, 'end'].get(
            'dateTime', Data.loc[i, 'end'].get('date')).replace("T", " ")
        tdelta = datetime.strptime(
            end[:-6], time_format) - datetime.strptime(start[:-6], time_format)
        income += calc_income(tdelta, float(hour_wage))

    print("{} : {}".format(name, int(income)))


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
    print('income from times rent a car')
    events_result = service.events().list(calendarId='primary', timeMin=Min,
                                          timeMax=Max, singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    Data = pd.DataFrame(events)

    for i in range(len(keyword.columns)):
        get_working(Data, keyword.iloc[0, i], keyword.iloc[1, i])


if __name__ == "__main__":
    main()
