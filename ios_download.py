import sys
import telnetlib
import os


def dwnld(ip,port,Username,file_path,tftp_server_ip,tn):

    file_name = os.path.basename(file_path)
    print(file_name)

    #tn = telnetlib.Telnet(ip,port)
    #tn.open(ip,port)
    try:
        #tn = telnetlib.Telnet(ip,port)
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        tn.write(b"\n")

    #cat9k_iosxe.17.03.02a.SPA.bin
    #特権モードにいる前提


        while True:
                try:
                    print("Finding out " + "\"" + file_name + "\"" + " in flash...")
                    #guruguru.spinner_gen()
                    tn.write(b"dir " + file_name.encode('ascii') + b"\n")
                    output_dir = tn.read_until(b"No such file", 3)

                #    print(output_dir.decode('ascii'))
                except EOFError as e:
                    print("Connection closed: %s") % e

                if b"No such file" in output_dir:
                    print("The target version image will be downloaded")
                    print("Checking reachability to TFTP Server in progress...")
                    tn.write(b"ping " + b"vrf Mgmt-vrf " + tftp_server_ip.encode('ascii') + b"\n")
                    tn.read_until(tftp_server_ip.encode('ascii'))
                    output_ping = tn.read_until(b"!!!!!",5)


                    if b"!!!!!" in output_ping:
                        print("TFTP Server is reachable")
                        print('Starting download...')

                        if b"bootflash:" in output_dir:
                            tn.write(b"copy tftp: bootflash:" + b" " + b"vrf Mgmt-vrf" + b"\n")
                            tn.read_until(b"Address or name of remote host",2)
                            tn.write(tftp_server_ip.encode('ascii') + b"\n")
                            tn.read_until(b"Source filename",2)
                            tn.write(file_path.encode('ascii') + b"\n")
                            tn.read_until(b"Destination filename",2)
                            tn.write(b"\n")
                            tn.write(b"\n")
                            tn.read_until(b"?",2)
                            checking_accessing = tn.read_until(file_name.encode('ascii') + b"...", 3)
                            print(checking_accessing.decode('ascii'))
                            tn.write(b"\n")
                            tn.write(b"\n")
                            tn.write(b"\n")
                            output_copy = tn.read_until(b'[OK',2)
                            #sample.main()
                            if b'[OK' in output_copy:
                                print('Downloaded successfully!!!')
                                continue

                            else:
                                print('Failed to download.')
                                break

                    elif b"does not exist" in output_ping:
                        print(output_ping.decode('ascii'))
                        break

                    elif b"%" in output_ping:
                        print("%%%")
                        break

                    else:
                        print("Error: Unreachable to TFTP Server")
                        break

                elif file_name.encode('ascii') in output_dir:
                    print("the target file exists in this device.")
                    tn.write(b"dele bootflash:test.txt")
                    tn.write(b"\n")
                    tn.write(b"\n")
                    break

                else:
                    print("Error")
                    break

        #tn.close()

    except EOFError:
        print("Connection closed by EOFError...")
