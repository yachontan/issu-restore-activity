import sys
import telnetlib

#Telent

TELNET_HOST = "10.71.140.56"
TELNET_PORT = "2006"

try:
    tn = telnetlib.Telnet(TELNET_HOST, TELNET_PORT)
#    f_log.write("\n---- " + HOST_NAME + "( telnet " + TELNET_HOST + " " + TELNET_PORT +" ) ----\n")
    tn.write(b"\r")
    tn.write(b"\r")
    tn.write(b"\r\n")
#    tn.write(b"conf" + b" " + b"t")
    tn.write(b"\n")
#    tn.write(b"hostname RRR")
    tn.write(b"\n")

#cat9k_iosxe.17.03.02a.SPA.bin
#特権モードにいる前提
    try:
        print("Finding out the target version image >")
        target_file = sys.stdin.readline().rstrip()
        #tn.write(b"dir bootflash:" + target_file.encode('ascii') + b"\n")
        tn.write(b"dir " + target_file.encode('ascii') + b"\n")
        #prompt_def = tn.read_until(b">", 3)
        output_dir = tn.read_until(b"(No such file or directory)", 3)
    except EOFError as e:
        print("Connection closed: %s") % e
    #print("#####")
    #print(target_file.encode('ascii')) #-> b'cat9k_iosxe.17.03.02a.SPA.bin\n'
    #print(target_file.encode('ascii').decode('ascii'))
    #print(target_file)

    if b"(No such file or directory)" in output_dir:
        print("The target version image will be downloaded")

        print("Checking reachability to TFTP Server in progress...")
        SERVER_IP = "10.71.136.1"
        #SERVER_IP = "192.168.203.1"
        FILE_PATH = "/yatogash/test.txt"

        tn.write(b"ping " + b"vrf Mgmt-vrf " + SERVER_IP.encode('ascii') + b"\n")
        #tn.write(b"ping " + SERVER_IP.encode('ascii') + b"\n")
        ping_result = tn.read_until(b"!!!!!",5)

        #print(b"ping " + b"vrf Mgmt-vrf " + SERVER_IP.encode('ascii') + b"\n")


        if b"!!!!!" in ping_result:
            print("TFTP Server is reachable")
            print('Starting download...')

            if b"bootflash:" in output_dir:
                tn.write(b"copy tftp:// bootflash:" + b" " + b"vrf Mgmt-vrf" + b"\n")
                tn.read_until(b"Address or name of remote host",2)
                tn.write(SERVER_IP.encode('ascii') + b"\n")
                tn.read_until(b"Source filename",2)
                tn.write(FILE_PATH.encode('ascii') + b"\n")
                tn.read_until(b"Destination filename",2)
                tn.write(b"\n")

            #    process_log = read_until(b"Accessing",2)
            #    if b"Accessing" +
                #Accessing tftp://10.71.136.1/yatogash/test.txt...



        #    pass

        elif b"does not exist" in ping_result:
            print("vrf does not exist")

        elif b"%" in ping_result:
            print("%%%")

        else:
            print("Error: Unreachable to TFTP Server")
            #break

    elif target_file.encode('ascii') in output_dir:
        print("the target file is exist")





    else:
        print("Error")
#   - show version
#   - if not exist 17.3.2a
#     - send command "dir bootflash:17.3.2a.bin"
#     - get result the command
#       - if result is equal Terget IOS-XE version name(XXX.bin)
#         - pass
#        - else
#          - download IOS fro TFTP



except EOFError:
    print("Connection closed by EOFError...")
