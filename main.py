#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FileName: 	calc_income
# CreatedDate:  2018-06-02 13:44:24 +0900
# LastModified: 2018-09-26 13:35:50 +0900
#

import argparse
import os
import re
from datetime import datetime

import pandas as pd
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file

# myfunc
from graph import Graph
from working import Working


def main():
    # option
    parser = argparse.ArgumentParser(
        description='calculation income from google calendar')
    parser.add_argument(
        '-m',
        '--month',
        metavar='YYYY-MM',
        action='store',
        nargs='?',
        help='choice month',
        default=datetime.now().strftime("%Y-%m"))
    parser.add_argument(
        '-g',
        '--graph',
        metavar='YYYY',
        action='store',
        nargs='?',
        help='choice year for graph',
        const=datetime.now().strftime("%Y"))
    args = parser.parse_args()

    # variable
    input_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'input')
    jobs_path = os.path.join(input_path, 'jobs.csv')
    credentials_path = os.path.join(input_path, 'credentials.json')
    keyword = pd.read_csv(jobs_path)
    year = int(re.sub(r"-.*$", "", args.month))
    month = int(re.sub(r"^.*-", "", args.month))

    # Setup the Calendar API
    store = file.Storage(credentials_path)
    creds = store.get()
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    working = Working(service, year, month)

    print(args.month)
    for i in range(len(keyword.index)):
        name, income = working.get_working(
            keyword.loc[i, 'name'], keyword.loc[i, 'hour_wage'],
            keyword.loc[i, 'start_day'], keyword.loc[i, 'transport_expense'])
        print("{} : {}".format(name, income))

    # make graph
    if args.graph is not None:
        graph = Graph(service, keyword)
        graph.make_graph(int(args.graph))


if __name__ == "__main__":
    main()
