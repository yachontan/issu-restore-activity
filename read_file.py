# -*- coding: utf-8 -*-
import os
import csv
import sys
import datetime

csv_contents = "Telnet-list.csv"

def csv_read(csv_contents):
    csv_file = open(csv_contents, "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    csv_list = []
    #Split up header and data
    #skip header
    header = next(f)
    #input csv_list from next(f)
    csv_list = [row for row in f]
    return csv_list
 

def txt_read(txt_contents):
    txt_list = []
    f = open(txt_contents)
    #for row in f:
    txt_list = f.read().splitlines()
    f.close()
    return txt_list
