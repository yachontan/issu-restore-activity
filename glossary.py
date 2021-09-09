import datetime
import telnetlib
import os
import sys

def get_time_file():
    # Expect to use for filename
    dt_now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S%f')
    return dt_now

def get_time_log():
    # Expect to use for outputting logs
    dt_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    return dt_now

def set_telnet_log_name(ip,port,title):
    #Output telnet log
    log_name = ip + "_" + port + "_" + get_time_file() + "_" + title + ".txt"
    return log_name

def telnet_log(log_name,log_output):
    f = open(log_name, mode='a', newline="", encoding="ms932")
    if "#" in log_output:
        f.write(str(log_output))
    else:
        f.write(str(log_output) + "\n")
    f.close()

def terminal_log(log_name,log_output):
    s = "[terminal]"+ get_time_log() +": "+ log_output
    f = open(log_name, mode='a', newline="", encoding="ms932")
    f.write(str("\n"+s) +"\n-------------------\n")
    f.close()
    return print(s)
