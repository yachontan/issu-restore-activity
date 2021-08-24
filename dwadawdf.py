import sys
import telnetlib

#Telent

TELNET_HOST = "10.71.140.56"
TELNET_PORT = "2030"

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


    try:
        print("Waiting for prompt")
        prompt_def = tn.read_until(b">", 3)
    except EOFError as e:
        print("Connection closed: %s") % e

    while b">" in prompt_def:
        if b">" in prompt_def:
        #1
        #Router>
        #-> execute “en”
            #A
            tn.write(b"enable" + b"\n")
            prompt_en = tn.read_until(b"#",3)
            print("enable command is executed") #消す予定

            if b"#" in prompt_en:
            #    1-a
            #    Router#
            #    -> OK
                print("Done: Moved to privileged EXEC mode successfully!!!")
                tn.write(b"exit")    #消す予定

            elif b"Password" in prompt_en:
            #    1-b
            #    Password:
            #    -> input password
                #for i in range(3,1):
                #    i = i - 1
                i = 3
                print("Input enable password" + "  (" + str(i) + " times left) >")
                #B
                while b"Password" in prompt_en:
                    en_pwd = sys.stdin.readline() #パスワード入力プロンプト
                    i = i - 1
                    tn.write(en_pwd.encode('ascii') + b"\n")
                    prompt_en_pwd = tn.read_until(b"#",2)
                    print("Inputed the password.")  #消す予定
                #    print(i)

                    if b"#" in prompt_en_pwd:
                #        1-b-1
                #        Router#
                #        -> OK
                        print("Done: Moved to privileged EXEC mode successfully!!!")
                        tn.write(b"exit")    #消す予定
                        break


                    elif b"Password" in prompt_en_pwd:
                        #for i in range(1,3):
                    #        1-b-2
                    #        Password:
                    #        -> input pass again
                        if i == 1:
                            print("Error: Password is incorrect...\n" + "Input enable password correctly" + "  (" + str(i) + " time left) > ")
                            continue
                            #Bに戻る

                        else:
                            print("Error: Password is incorrect...\n" + "Input enable password correctly" + "  (" + str(i) + " times left) > ")
                            continue

                    else:
                        print("Error: Incorrest password was entered 3 times and refused, run the process again.")
                    #        1-b-3
                    #        % Bad passwords
                    #        -> print (Try again) and back to 1
                        break
                         #Aに戻る or 終了させる。

            continue
            #     else:
            #         pass
                #        print("xxxxxx")
                #ケースが思いつかない。なければ、No Action.





        elif b")#" in prompt_def:
        #3
        #Router(xx)#
        #-> execute “end”
            tn.write(b"end")
            prompt_end = tn.read_until(b"#",3)
            print("end command is executed")    #消す予定



            if b")#" in prompt_end:
              print('Error: Terminal is too busy, fix your router to run the process.')


            elif b"#" in prompt_end:
              #   3-a
              #   Router#
              #   -> O
              print('Done: Moved to privileged EXEC mode successfully!!!')

            else:
              #   3-b
              #   other
              #-> print (Terminal is too busy,Fix your router to run the process.)
              print('Error: Terminal is too busy, fix your router to run the process.')




        elif b"#" in prompt_def:
        #2
        #Router#
        #-> OK
            print('Done: Moved to privileged EXEC mode successfully!!!')
            tn.write(b"exit")   #消す予定

        elif b"%" in prompt_def:
            prinit("%%%%")
            tn.write(b"\r\n")

        else:
        #4
        #other
        #-> print (Terminal is too busy,Fix your router to run the process.)
            print('Error: Terminal is too busy, fix your router to run the process.')
            tn.write(b"\r\n")
            tn.write(b"\r")
            tn.write(b"\n")

except EOFError:
    print("Connection closed by EOFError...")
