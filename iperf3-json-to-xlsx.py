#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- mode: python; python-indent-offset: 4 -*-
#
# iperf3-json-to-xlsx.py --dir directory_name
#   is directory_name is . it proces the current directory
#
# The program outputs a file named: experiments.xlsx
# with each input JSON file as a sheet and with all of the data collected on an sheet named: All
#
# The program assumes that there are a set of files produced by iPerf3 with the --json argument
# and that names of the files have the form: CONGESTIONCTRL_RATE_DELAY_LOSS
# where CONGESTIONCTRL might be bbr, reno, etc.
#       RATE might be 100mbit or simply 100 (both for 100 Mbps)
#       DELAY is the delay in ms (as an integer without units)
#       LOSS is the loss probability (as an integer) 
#
# 2022-04-06
# G. Q. Maguire Jr.
#

import re
import sys
import subprocess

import json
import argparse
import os			# to make OS calls, here to get time zone info


# Use Python Pandas to create XLSX files
import pandas as pd

import pprint

import time
import datetime
import isodate                  # for parsing ISO 8601 dates and times
import pytz                     # for time zones
from dateutil.tz import tzlocal

def main(argv):
    global Verbose_Flag
    global testing
    global args



    argp = argparse.ArgumentParser(description="iperf3-json-to-xlsx.py: to iPerf3 JSON files and make XLSX files")

    argp.add_argument('-v', '--verbose', required=False,
                      default=False,
                      action="store_true",
                      help="Print lots of output to stdout")

    argp.add_argument('-t', '--testing',
                      default=False,
                      action="store_true",
                      help="execute test code"
                      )

    argp.add_argument('-j', '--json',
                      type=str,
                      default=None,
                      help="JSON file for extracted data"
                      )

    argp.add_argument('--dir',
                      type=str,
                      default=None,
                      help="directory name for json files"
                      )

    args = vars(argp.parse_args(argv))

    Verbose_Flag=args["verbose"]

    testing=args["testing"]
    if Verbose_Flag:
        print("testing={}".format(testing))

    dir_name=args['dir']
    if not dir_name:
        print("no directory specified")
        return

    collected_df=pd.DataFrame() # create empty data dataframe
    collected_start_df=pd.DataFrame() # create empty data dataframe

    writer = pd.ExcelWriter('experiments.xlsx', engine='xlsxwriter')

    for file in os.listdir(dir_name):
        if file.endswith(".json"):
            file_name=os.path.join(dir_name, file)
            print("processing file: {}".format(file_name))
            try:
                with open(file_name, 'r') as json_FH:
                    try:
                        json_string=json_FH.read()
                        dict_of_json=json.loads(json_string)
                    except:
                        print("Error in reading={}".format(json_string))
                        return
            except:
                print("Error in opening file={}".format(file_name))
                continue


            if Verbose_Flag:
                print("read JSON: {}".format(dict_of_json))
            # The measurement data is in 'intervals'
            intervals_data=dict_of_json['intervals']
            intervals_df=pd.json_normalize(intervals_data)
            # the name of the JSON file has the form: CONGESTIONCTRL_RATE_DELAY_LOSS
            new_column_names='CONGESTIONCTRL_RATE_DELAY_LOSS'.split('_')
            file_name_trimmed=file_name[len(dir_name)+1:-5]
            new_col_values=file_name_trimmed.split('_')
            if Verbose_Flag:
                print("file_name_trimmed=={0}; new_column_names={1}; new_col_values={2}".format(file_name_trimmed, new_column_names, new_col_values))
            for index,  ncn in enumerate(new_column_names):
                if index==0:
                    intervals_df[ncn]=new_col_values[index]
                else:
                    val=new_col_values[index]
                    if val.endswith('mbit'):
                        val=val.replace('mbit', '')
                    intervals_df[ncn]=float(val)
            collected_df=collected_df.append(intervals_df)
            name_for_sheet=file_name.replace("_", " ")[len(dir_name)+1:-5]

            start_data=dict_of_json['start']
            start_df=pd.json_normalize(start_data)
            start_df['run name']=name_for_sheet
            collected_start_df=collected_start_df.append(start_df)

            intervals_df.to_excel(writer, sheet_name=name_for_sheet)

    collected_df.to_excel(writer, sheet_name='All')
    collected_start_df.to_excel(writer, sheet_name='Starting')

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

