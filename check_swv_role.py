import sys
import telnetlib
import os
import time


def check_role(ip,port,tn):


    try:
        #tn = telnetlib.Telnet(ip,port)
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        tn.write(b"\n")


        while True:
                try:

                    print("Finding out the role of this switch...")
                    output_initial = tn.read_until(b"e3e3e3",3)

                #    print(output_dir.decode('ascii'))
                except EOFError as e:
                    print("Connection closed: %s") % e

                if b"-stby>" in output_initial or b"-stby#" in output_initial:
                    print("This switch is STANDBY of the stack")
                    print("Waiting for booting and switching to Active...")

                    print("")






                elif b">" in output_initial or b"#" in output_initial:#active
                    print("This switch is ACTIVE")
                    break

                elif b"rommon " in output_initial and b">" in output_initial:#rommon
                    print("This switch is in ROMMON mode now, recover it.")
                    break

                else:
                    print("This switch is ICS of the stack")
                    print("Waiting for booting and switching to Active...")

                    ics_log1 = tn.read_until(b"ICS: Received ICS reload from in-chassis active. Rebooting")
                    print(ics_log1.decode('ascii'))

                    ics_log2 = tn.read_until(b"ICS: Received ICS reload_now from ICA. Rebooting")
                    print(ics_log2.decode('ascii'))

                    init_hw = tn.read_until(b"Initializing Hardware...")
                    print(init_hw.decode('ascii'))

                    output_rommon = tn.read_until(b"sss",3)
                    if b"rommon 1 >" in output_rommon:
                        print("rommon mode now, Recover it")
                        break


                    else:
                        while True:
                            progress_log = tn.read_until(b'#',1)
                            ###progress_log = tn.read_some()
                            if b"#" in progress_log:
                                print("#", end='', flush=True)
                                continue
                            else:
                                print('break')
                                break
                                
                        tn.read_until(b"Restricted Rights Legend")
                        print("switch will be up soon")

                        tn.read_until(b"Press RETURN to get started!")
                        tn.write(b"\r")
                        tn.write(b"\r")
                        tn.write(b"\r\n")
                        tn.write(b"\n")
                        tn.write(b"\n")

                        continue




                    ############

        #tn.close()

    except EOFError:
        print("Connection closed by EOFError...")
