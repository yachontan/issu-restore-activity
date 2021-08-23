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
telnet_list = read_file.csv_read(lineinput)
print(telnet_list)


lineinput = "show.txt"
show_list = read_file.txt_read(lineinput)
print(show_list)

#telnet from i of host_list
f = []
#for i in range(len(csv_list)):
#for i in range(len(csv_list)) :
#  if i > 1:
#    print(i)
#    dotelnet.main(i[0],i[1],i[2],i[3],i[4])
    
    
#    tn = telnetlib.Telnet(i[0], i[1])

# prompt.py

# <message>

# 