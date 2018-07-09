# zaim
calculation income from google calendar

## Preparation
After authentication with OAuth with reference to [How to authorize](https://developers.google.com/calendar/quickstart/python?hl=ja#step_3_set_up_the_sample), please make `input/jobs.csv`.
```csv:key.csv
name,hour_wage,start_day,transport_expense,id
hoge,1000,11,500,hoge1
geho,1500,1,0,GEHO
```

## Usage
```sh:main.py
usage: main.py [-h] [-m [YYYY-MM]] [-g [YYYY]]

calculation income from google calendar

optional arguments:
  -h, --help            show this help message and exit
  -m [YYYY-MM], --month [YYYY-MM]
                        choice month
  -g [YYYY], --graph [YYYY]
                        choice year for graph
```

## Example
By default, income in current month is displayed.
```sh
% python3 main.py
```

Output annual salary as graph.
```sh
% python3 main.py -g
```
