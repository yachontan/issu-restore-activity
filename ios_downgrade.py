import sys
import telnetlib
import os
import time
import glossary
import datetime

def save_config(tn,log_name):
    glossary.terminal_log(log_name,"Save the configuration to startup-config...")
    tn.write(b"write memory"+ b"\n")
    glossary.telnet_log(log_name,tn.read_until(b"[OK]").decode("ascii"))
    glossary.terminal_log(log_name,"Done save configuration..." )
    glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))
    tn.write(b"\n")
    glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))

def reload_method(tn,log_name):
    # Execute reload
    glossary.terminal_log(log_name,"Execute reload...")
    tn.write(b"reload"+ b"\n")
    glossary.telnet_log(log_name,tn.read_until(b"Proceed with reload? [confirm]").decode("ascii"))
    tn.write(b"\n")
    glossary.telnet_log(log_name,tn.read_until(b"Reload requested by console. Reload Reason: Reload Command.").decode("ascii"))
    glossary.terminal_log(log_name,"Start to reload...")

def initial_dialog_abort(tn,log_name):
    glossary.terminal_log(log_name,"Abort initial dialog...")
    try:
        while tn.read_until(b"Would you like to enter the initial configuration dialog? [yes/no]:",900):
            tn.write(b"no"+ b"\n")
            glossary.telnet_log(log_name,tn.read_until(b"Would you like to terminate autoinstall? [yes]:").decode("ascii"))
            tn.write(b"yes"+ b"\n")
            glossary.telnet_log(log_name,tn.read_until(b"Press RETURN to get started!").decode("ascii"))
            tn.write(b"\n") 
            glossary.terminal_log(log_name,"Aborted initial dialog...")          
            glossary.telnet_log(log_name,tn.read_until(b"Guestshell destroyed successfully").decode("ascii"))       
            break
    except KeyboardInterrupt: 
        # if Ctl+C
        glossary.terminal_log(log_name,":\nInterrupt")

    glossary.terminal_log(log_name,"Wait for bringing up system...")
    for i in range(0, 20, 1):
        # Wait boot method is done...
        time.sleep(30)
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        if i >= 15 :
            tn.write(b"\r")
            tn.write(b"\r")
            tn.write(b"\r\n")
            tn.write(b"\n")
            tn.write(b"sh ver | include System image file\n") 
            if (tn.read_until(b"System image file is",10)):
                glossary.terminal_log(log_name,"Resume this program now...")
                tn.write(b"\n")
                glossary.telnet_log(log_name,tn.read_until(b">").decode("ascii"))
                break
            else:
                glossary.terminal_log(log_name,"Wait another 30 sec...")
                time.sleep(30)
                continue
        else:
            glossary.terminal_log(log_name,"Waiting "+ str(i*30) +" sec now...")
            continue

def dwngrd(ip,port,file_path,en_password,tn):
    log_name = glossary.set_telnet_log_name(ip,port,"ios_upgrade")
    
    file_name = os.path.basename(file_path)
    print(file_name)

    try:
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        tn.write(b"\n")

        # Should be executed after done check target ios is exsited or not in s  up)
        glossary.terminal_log(log_name,"Downgrade IOS to " + "\"" + file_name + "\"" + " is started...")
        
        # Change to configration mode
        glossary.terminal_log(log_name,"Change to configration mode...")
        tn.write(b"conf t"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"(config)#").decode("ascii"))
        tn.write(b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"(config)#").decode("ascii"))

        # Delete packages.conf and change boot method to legacy
        glossary.terminal_log(log_name,"Delete packages.conf and change boot method to legacy...")
        tn.write(b"\n")
        tn.write(b"no boot system"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"(config)#").decode("ascii"))
        tn.write(b"end"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))
        
        # Save the config to startup-config
        save_config(tn,log_name)

        # Delete all config in switch
        glossary.terminal_log(log_name,"Delete all config in switch...")
        tn.write(b"\n")
        tn.write(b"write erase"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"[confirm]").decode("ascii"))
        tn.write(b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"complete").decode("ascii"))
        tn.write(b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))
        tn.write(b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))

        # Execute reload
        reload_method(tn,log_name)

        # Wait reload until prompt shows "rommon 1 >"
        glossary.telnet_log(log_name,tn.read_until(b"Initializing Hardware...").decode("ascii")) 
        glossary.terminal_log(log_name,"Wait until prompt shows [rommon 1 >] ...")
        glossary.telnet_log(log_name,tn.read_until(b"rommon 1 >",900).decode("ascii"))
        tn.write(b"boot bootflash:" + file_name.encode('ascii') + b"\n")
        glossary.terminal_log(log_name,tn.read_until(b"boot: reading file "+ file_name.encode('ascii')).decode("ascii"))
        glossary.terminal_log(log_name,"Start to boot target IOS...")
        
        # Wait reload until initial dialog and abort all
        initial_dialog_abort(tn,log_name)

        # Change to enable mode
        glossary.terminal_log(log_name,"Change to enable mode...")
        tn.write(b"enable"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))
        tn.write(b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))

        # Execute command [install remove inactivate]
        glossary.terminal_log(log_name,"Execute command [install remove inactive] and remove old packages...")
        tn.write(b"install remove inactive"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"install_remove: START").decode("ascii"))
        glossary.terminal_log(log_name,"Start install_remove...")
        glossary.telnet_log(log_name,tn.read_until(b"Do you want to remove the above files? [y/n]").decode("ascii"))
        tn.write(b"y"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))
        glossary.terminal_log(log_name,"Done to remove inactive packages all...")


        # Change to configuration mode and set packages.conf in config file
        glossary.terminal_log(log_name,"Change to configuration mode and set packages.conf in config file...")
        tn.write(b"conf t"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"(config)#").decode("ascii"))
        tn.write(b"boot system bootflash:packages.conf"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"(config)#").decode("ascii"))
        tn.write(b"end"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"#").decode("ascii"))

        # Save the config to startup-config
        save_config(tn,log_name)

        # Execute command [install add file <filename> activate commit]
        glossary.terminal_log(log_name,"Execute command install add file <filename> activate commit")
        tn.write(b"install add file bootflash:" + file_name.encode('ascii') + b" activate commit"+ b"\n")

        # Confirm to reload and change boot to install mode
        glossary.terminal_log(log_name,"Confirm to reload and change boot method to install mode...")
        glossary.telnet_log(log_name,tn.read_until(b"install_add_activate_commit: Adding PACKAGE").decode("ascii"))
        glossary.terminal_log(log_name,"Done install_add_activate_commit: Adding PACKAGE")

        #tn.read_until(b"Please confirm you have changed boot config to bootflash:packages.conf [y/n]")
        #tn.write(b"y"+ b"\n")
        #tn.read_until(b"This operation may require a reload of the system. Do you want to proceed? [y/n]")

        glossary.telnet_log(log_name,tn.read_until(b"[y/n]").decode("ascii"))
        tn.write(b"y"+ b"\n")
        glossary.telnet_log(log_name,tn.read_until(b"Starting Add").decode("ascii"))
        glossary.terminal_log(log_name,"--- Starting Add ---")
        glossary.telnet_log(log_name,tn.read_until(b"Finished Add",900).decode("ascii"))
        glossary.terminal_log(log_name,"--- Finished Add ---")
        glossary.telnet_log(log_name,tn.read_until(b"This operation may require a reload of the system. Do you want to proceed? [y/n]",900).decode("ascii"))
        tn.write(b"y"+ b"\n")
        glossary.terminal_log(log_name,"Proceeded switch reload...")
       
    #if glossary.telnet_log(log_name,tn.read_until(b"FAILED: install_add_activate_commit"):
    #        time.sleep(1)
    #        glossary.terminal_log(log_name,"Faild command. Re-execute command install add file <filename> activate commit")
    #        tn.write(b"install add file bootflash:" + file_name.encode('ascii') + b" activate commit"+ b"\n")
    #        glossary.telnet_log(log_name,tn.read_until(b"Please confirm you have changed boot config to bootflash:packages.conf [y/n]")
    #        tn.write(b"y"+ b"\n")
    #        glossary.telnet_log(log_name,tn.read_until(b"--- Starting Add ---")
    #       glossary.terminal_log(log_name,"--- Starting Add ---")
    #   glossary.telnet_log(log_name,tn.read_until(b"Starting Activate")
    #   glossary.terminal_log(log_name,"--- Starting Activate ---")
    #   glossary.telnet_log(log_name,tn.read_until(b"Finished Activate")
    #   glossary.terminal_log(log_name,"Finished Activate")
    #   glossary.telnet_log(log_name,tn.read_until(b"Starting Commit")
    #   glossary.terminal_log(log_name,"--- Starting Commit ---") 
    #   glossary.telnet_log(log_name,tn.read_until(b"Finished Commit")
    #   glossary.terminal_log(log_name,"Finished Commit")

        glossary.telnet_log(log_name,tn.read_until(b"SUCCESS: install_add_activate_commit",900).decode("ascii"))
        glossary.terminal_log(log_name,"SUCCESS: install_add_activate_commit...")

        # Wait until initial dialog and abort all
        glossary.telnet_log(log_name,tn.read_until(b"reload action requested").decode("ascii"))
        glossary.terminal_log(log_name,"Reloading now...")

        # Verify
        glossary.telnet_log(log_name,tn.read_until(b"Press RETURN to get started!",900).decode("ascii"))
        glossary.terminal_log(log_name,"Wait 120 sec for bringing up systems...")
        time.sleep(120)
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        tn.write(b"sh ver | include System image file\n") 
        glossary.telnet_log(log_name,tn.read_until(b'"bootflash:packages.conf"').decode("ascii"))
        glossary.terminal_log(log_name,"Done downgrade IOS...")

        # Output telnet log
        #glossary.telnet_log(ip,port,tn,name ="ios_upgrade")

    except EOFError:
        glossary.terminal_log(log_name,"Connection closed by EOFError...")



