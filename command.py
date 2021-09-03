import datetime
import read_file

def output_show(ip,port,show_list,tn):

    dt_now = datetime.datetime.now()
    log_output = ip + "_" + port + "_" + dt_now.strftime('%Y%m%d-%H%M%S-%f') + "_" + "show_result.txt"
    
    print("Commands in '", show_list,"' will be issued.")
    command_list = read_file.txt_read(show_list)
    
    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.read_until(b"#")
    tn.write(b"terminal length 0\n")
    tn.read_until(b"#")
    tn.write(b"\n")

    for com in command_list:
        print("... " + com)
        tn.write(com.encode('ascii') + b"\n")

    tn.write(b"!!!!!! DONE !!!!!!" + b"\n")
    tn.write(b"terminal default length\n")
    output = tn.read_until(b"!!!!!! DONE !!!!!!").decode('ascii')

    tn.write(b"\n")
    tn.read_until(b"#")
    
    f_log = open(log_output,mode="w", newline="", encoding="ms932")
    f_log.write("\n---- (telnet " + ip + " : " + port +") ----\n")
    f_log.write(output)
    f_log.close()

    print("... Done!")
    print("### ", log_output, "is created.")


def input_conf(ip,port,config_list,tn):
    
    dt_now = datetime.datetime.now()
    log_output = ip + "_" + port + "_" + dt_now.strftime('%Y%m%d-%H%M%S-%f') + "_" + "config_result.txt"

    print("Commands in '", config_list,"' will be issued.")
    command_list = read_file.txt_read(config_list)

    tn.write(b"\r\n")
    tn.write(b"\r\n")
    tn.read_until(b"#")
    tn.write(b"configure terminal\n")
    tn.read_until(b"#")
    tn.write(b"\n")

    for com in command_list:
        print("... " + com)
        tn.write(com.encode('ascii') + b"\n")

    tn.write(b"end\n")
    tn.write(b"!!!!!! DONE !!!!!!" + b"\n")
    output = tn.read_until(b"!!!!!! DONE !!!!!!").decode('ascii')

    tn.write(b"\n")
    tn.read_until(b"#")
    
    f_log = open(log_output,mode="w", newline="", encoding="ms932")
    f_log.write("\n---- (telnet " + ip + " : " + port +") ----\n")
    f_log.write(output)
    f_log.close()

    print("... Done!")
    print("### ", log_output, "is created.")
