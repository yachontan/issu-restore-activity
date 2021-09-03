import os
import csv
import sys
import datetime
import telnetlib
import read_file
import dotelnet
import prompt
import ios_download


#import prompt

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

  tn = telnetlib.Telnet(ip,port)
  prompt.enable(ip,port,Username,tel_password,en_password,tn)
  ios_download.dwnld(ip,port,en_password,target_ios,tftp_server,tn)

#print("dummy2")
# Example to make a list[] from txt
parameter = read_file.txt_read(show_list)
print(parameter)





#dotelnet.main(ip,port,Username,tel_password,en_password)

#prompt.enable(ip,port,Username,tel_password,en_password,tn)

#ios_download.dwnld(ip,port,en_password,target_ios,tftp_server)
