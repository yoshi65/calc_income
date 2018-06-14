#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	working
# CreatedDate:  2018-06-04 11:34:30 +0900
# LastModified: 2018-06-14 14:32:10 +0900
#


import os
import sys
import numpy as np
import pandas as pd
from apiclient.discovery import build
from datetime import datetime, timedelta


class Working():

    def __init__(self, service, year, month):
        # variable
        self.service = service
        self.time_format = "%Y-%m-%d %H:%M:%S"
        self.year = year
        self.month = month

    def calc_income(self, tdelta, hour_wage):
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

    def get_working(self, name, hour_wage, start_day, transport_expense):
        # variable
        income = 0
        year = self.year
        month = self.month + 1
        if self.month == 12:  # cross over the years
            year = self.year + 1
            month = 1
        Min = datetime(self.year, self.month, start_day).isoformat() + 'Z'
        Max = (datetime(year, month, start_day) -
               timedelta(days=1)).isoformat() + 'Z'

        # Call the Calendar API
        events_result = self.service.events().list(calendarId='primary', timeMin=Min,
                                                   timeMax=Max, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        # Convert to DataFormat
        Data = pd.DataFrame(events)
        Data = Data[Data['summary'] == name].reset_index(drop=True)

        for i in range(len(Data.index)):
            start = Data.loc[i, 'start'].get(
                'dateTime', Data.loc[i, 'start'].get('date')).replace("T", " ")
            end = Data.loc[i, 'end'].get(
                'dateTime', Data.loc[i, 'end'].get('date')).replace("T", " ")
            tdelta = datetime.strptime(
                end[:-6], self.time_format) - datetime.strptime(start[:-6], self.time_format)
            income += self.calc_income(tdelta,
                                       float(hour_wage)) + transport_expense * 2

        return [name, int(income)]
