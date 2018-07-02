#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	graph
# CreatedDate:  2018-06-26 16:52:53 +0900
# LastModified: 2018-06-29 17:42:05 +0900
#


import os
import sys
import numpy as np
import pandas as pd
from apiclient.discovery import build
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import ticker

# myfunc
from working import Working


class Graph():

    def __init__(self, service, keyword):
        # read argument
        self.service = service
        self.keyword = keyword

        # setting matplotlib
        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')

        # output path
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.output_path = os.path.join(self.dir_path, "output")

        # set output directory
        try:
            os.mkdir(self.output_path)
        except FileExistsError:
            pass

    def make_graph(self, year):
        # variable
        output_name = os.path.join(
            self.output_path, "income_{}.pdf".format(str(year)))
        month_list = [12] + list(range(1, 12))
        month_list_label = range(1, 13)

        # make income list equal the number of jobs
        income_list = [[] for i in range(0, len(self.keyword.index))]

        # arrange data
        for month in month_list:
            if month == 12:
                working = Working(self.service, year - 1, month)
            else:
                working = Working(self.service, year, month)

            for i in range(0, len(self.keyword.index)):
                name, income = working.get_working(
                    self.keyword.loc[i, 'name'], self.keyword.loc[i, 'hour_wage'], self.keyword.loc[i, 'start_day'], self.keyword.loc[i, 'transport_expense'])
                income_list[i].append(income)

        # draw graph
        ran = np.arange(len(month_list))
        width = 0.3
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        before = [ 0 for i in range(0, len(income_list[0])) ]
        for i in range(0, len(self.keyword.index)):
            ax.bar(ran, income_list[i], width=width, label="{} {}yen".format(self.keyword.loc[i, 'id'], str(sum(income_list[i]))), bottom=before)
            if sum(before) == 0:
                before = income_list[i]
            else:
                before += income_list[i]

        plt.xlabel(r"month", fontsize=16)
        plt.ylabel(r"money [yen]", fontsize=16)
        plt.legend(loc="best")
        plt.xticks(ran, month_list_label)
        plt.tight_layout()
        plt.savefig(output_name)
        plt.close(fig)
