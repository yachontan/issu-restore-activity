import sys
import telnetlib
import os
import time


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
                    output_dir = tn.read_until(b"No such file",2)

                #    print(output_dir.decode('ascii'))
                except EOFError as e:
                    print("Connection closed: %s") % e

                if b"No such file" in output_dir:
                    print("The target version image will be downloaded")
                    print("Checking reachability to TFTP Server in progress...")
                    tn.write(b"ping " + b"vrf Mgmt-vrf " + tftp_server_ip.encode('ascii') + b"\n")
                    tn.read_until(tftp_server_ip.encode('ascii'))
                    output_ping = tn.read_until(b"!!!!!",3)


                    if b"!!!!!" in output_ping:
                        print("TFTP Server is reachable")
                        print('Starting download...')

                        if b"bootflash:" in output_dir:
                            tn.write(b"copy tftp: bootflash:" + b" " + b"vrf Mgmt-vrf" + b"\n")
                            tn.read_until(b"Address or name of remote host")
                            tn.write(tftp_server_ip.encode('ascii') + b"\n")
                            tn.read_until(b"Source filename")
                            tn.write(file_path.encode('ascii') + b"\n")
                            tn.read_until(b"Destination filename")
                            #tn.write(b"\n")
                            tn.write(b"\n")
                            tn.read_until(b"?",2)
                            checking_accessing = tn.read_until(file_name.encode('ascii') + b"...", 3)
                            checking_loading = tn.read_until(file_name.encode('ascii') + b" from " + tftp_server_ip.encode('ascii'))
                            #eTaxMac.dmg from 10.71.136.1
                            print(checking_accessing.decode('ascii'))
                            print(checking_loading.decode('ascii') + "\n")
                            tn.write(b"\n")
                            tn.write(b"\n")
                            tn.write(b"\n")
                            ###tn.read_until(b":")


                            while True:
                                progress_log = tn.read_until(b'!',1)
                                ###progress_log = tn.read_some()
                                if b"!" in progress_log:
                                    print("!", end='', flush=True)
                                    continue
                                else:
                                    print('break')
                                    break


                            if b'[OK' in progress_log:
                                print('\n' + '...Downloaded successfully' + "\n")
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
                    #tn.write(b"dele bootflash:Cyberduck-7.9.2.34986.zip")
                    #tn.write(b"dele bootflash:eTaxMac.dmg")
                    tn.write(b"\n")
                    tn.write(b"\n")
                    break

                else:
                    print("Error")
                    break

        #tn.close()

    except EOFError:
        print("Connection closed by EOFError...")
