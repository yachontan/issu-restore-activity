# -*- coding: utf-8 -*-
import os
import csv
import sys
import telnetlib
import datetime


host = []
def main(ip,port,username,telnet_password,enable_password):

    print(ip)
    print(port)
    print(username)
    print(telnet_password)
    print(enable_password)

    tn = telnetlib.Telnet(ip, port)



#    tn.read_until("login: ")
#    tn.write(username + "\n")

# if password:
#     tn.read_until(b'Password: ')
#     tn.write(password.encode('ascii') + b'\n')
