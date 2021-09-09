import sys
import telnetlib

def enable(ip,port,username,telnet_password,enable_password,tn):
    #tn = telnetlib.Telnet(ip,port)

    try:
        #tn = telnetlib.Telnet(ip,port)
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        tn.write(b"\n")


        try:
            print("Waiting for prompt...")
            prompt_def = tn.read_until(b">", 3)
        except EOFError as e:
            print("Connection closed: %s") % e


        if b">" in prompt_def:
            print("Going to privileged EXEC mode...")
            tn.write(b"enable" + b"\n")
            prompt_en = tn.read_until(b"#",3)

            if b"#" in prompt_en:
                print("Done: Got to privileged EXEC mode successfully!!!")

            elif b"Password" in prompt_en:
                print("Going to privileged EXEC mode...")
                print("Getting password for privileged EXEC mode...")
                tn.write(enable_password.encode('ascii') + b"\n")
                prompt_en_pwd = tn.read_until(b"#",2)

                if b"#" in prompt_en_pwd:
                    print("Done: Got to privileged EXEC mode successfully!!!")

                elif b"Password" in prompt_en_pwd:
                    print('Error: Password is incorrect and refused, please coreect the password.')

                else:
                    print('Error: Terminal is too busy, fix your router to run the process.')

        elif b")#" in prompt_def:
            print('Going back to privileged EXEC mode...')
            tn.write(b"end")
            prompt_end = tn.read_until(b"#",3)

            if b")#" in prompt_end:
              print('Error: Terminal is too busy, fix your router to run the process.')

            elif b"#" in prompt_end:
              print('Done: Got back to privileged EXEC mode successfully!!!')

            else:
              print('Error: Terminal is too busy, fix your router to run the process.')

        elif b"#" in prompt_def:
            print("Done: In privileged EXEC mode NOW")

        elif b"%" in prompt_def:
            print("%%%%%ERROR%%%%%")
            tn.write(b"\r\n")

        else:
            print('Error: Terminal is too busy, fix your router to run the process.')
            tn.write(b"\r\n")
            tn.write(b"\r")
            tn.write(b"\n")




    except EOFError:
        print("Connection closed by EOFError...")
