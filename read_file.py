# -*- coding: utf-8 -*-
import os
import csv
import sys
import datetime


def csv_read(csv_contents):
## hostip -
## port - telnet tcp port 
## username - 
## password
# open file
    csv_file = open(csv_contents, "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    csv_list = []
    csv_list = [row for row in f]
    return csv_list
 

def txt_read(txt_contents):
   txt_list = []
   f = open(txt_contents)
   txt_list = f.readlines()
   f.close()
   return txt_list