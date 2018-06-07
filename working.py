#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	working
# CreatedDate:  2018-06-04 11:34:30 +0900
# LastModified: 2018-06-07 14:19:48 +0900
#


import os
import sys
import numpy as np
import pandas as pd
from datetime import datetime

class Working():

    def __init__(self, Data):
        # variable
        self.Data = Data
        self.time_format = "%Y-%m-%d %H:%M:%S"

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

    def get_working(self, name, hour_wage):
        # variable
        income = 0

        Data = self.Data[self.Data['summary']
                              == name].reset_index(drop=True)

        for i in range(len(Data.index)):
            start = Data.loc[i, 'start'].get(
                'dateTime', Data.loc[i, 'start'].get('date')).replace("T", " ")
            end = Data.loc[i, 'end'].get(
                'dateTime', Data.loc[i, 'end'].get('date')).replace("T", " ")
            tdelta = datetime.strptime(
                end[:-6], self.time_format) - datetime.strptime(start[:-6], self.time_format)
            income += self.calc_income(tdelta, float(hour_wage))

        return [name, int(income)]
