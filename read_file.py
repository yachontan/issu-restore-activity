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
#    csv_file = open('Telnet-list.csv', "r", encoding="ms932", errors="", newline="" )
    f = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    csv_list = []
    #Split up header and data
    #eader
    header = next(f)
    #
    csv_list = [row for row in f]
    return csv_list
 

def txt_read(txt_contents):
    txt_list = []
    f = open(txt_contents)
    for row in f:
     txt_list = f.read().splitlines()
    f.close()
#    for i in range(len(f2)):
#        txt_list[i] =f2[i].replace('\n','')
    return txt_list



#telnet_list = csv_read("Telnet-list.csv")
#print(telnet_list)