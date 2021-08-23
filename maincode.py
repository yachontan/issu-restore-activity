import os
import csv
import sys
import datetime
import telnetlib
import read_file
import dotelnet

# Check csv file is exist

# Read csv and put into host_list[]
lineinput = input("Input Telnet list file .csv:")
telnet_list = read_file.csv_read(lineinput)
print(telnet_list)

# set telnet list to each parameter
for i in range(len(telnet_list)):
  #defile param from telnet_list
  ip = telnet_list[i][0]
  port = telnet_list[i][1]
  Username = telnet_list[i][2]
  tel_password = telnet_list[i][3]
  en_password = telnet_list[i][4]
  config_list = telnet_list[i][5]
  show_list = telnet_list[i][6]
  target_ios = telnet_list[i][7]
  tftp_server = telnet_list[i][8]
  #Connect telnet
  tn = telnetlib.Telnet(ip,port,600)
  print(tn)
  tn.interact()
  
  # Close telnet
  tn.close()

# Example to make a list[] from txt
# lineinput = "show.txt"
# show_list = read_file.txt_read(lineinput)
# print(show_list)