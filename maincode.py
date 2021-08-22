import os
import csv
import sys
import datetime
import telnetlib
import read_file
import dotelnet

#Check csv file is exist

#read csv and put into host_list[]
lineinput = input("Input Telnet list file .csv:")
csv_list = read_file.csv_read(lineinput)
print(csv_list)

lineinput = "show.txt"
txt_list = read_file.txt_read(lineinput)
print(txt_list)

#telnet from i of host_list
i = []
for i in csv_list:
#    if i > 1:
  print(i)
#    dotelnet.main(i[0],i[1],i[2],i[3],i[4])
    
    
#    tn = telnetlib.Telnet(i[0], i[1])

# prompt.py

# <message>

# 