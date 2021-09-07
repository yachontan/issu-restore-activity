import sys
import telnetlib
import os

def initial_dialog_abort(tn):
    
    print("Abort initial dialog...")
    tn.read_until("Would you like to enter the initial configuration dialog? [yes/no]:")
    tn.write(b"no"+ b"\n")
    tn.read_until("Would you like to terminate autoinstall? [yes]:")
    tn.write(b"yes"+ b"\n")

def dwngrd(file_path,tn):

    file_name = os.path.basename(file_path)
    print(file_name)

    try:
        tn.write(b"\r")
        tn.write(b"\r")
        tn.write(b"\r\n")
        tn.write(b"\n")
        tn.write(b"\n")

    


        #cat9k_iosxe.17.03.02a.SPA.bin
        #Should be executed after done check target ios is exsited or not in s  up)

        print("Downgrade IOS to " + "\"" + file_name + "\"" + " is started...")

        # Change to configration mode
        print("Change to configration mode...")
        tn.write(b"conf t"+ b"\n")
        tn.read_until("(config)#")
        # Delete packages.conf and change boot method to legacy
        print("Delete packages.conf and change boot method to legacy...")
        tn.write(b"no boot system"+ b"\n")
        tn.read_until("(config)#")
        tn.write(b"end"+ b"\n")
        tn.read_until("#")

        # Save the config to startup-config
        print("Save the configuration to startup-config...")
        tn.write(b"write memory"+ b"\n")
        tn.read_until("#")

        # Delete all config in switch
        print("Delete all config in switch...")
        tn.write(b"write erase"+ b"\n")
        tn.read_until("[confirm]")
        tn.write(b"\n")
        tn.read_until("#")

        # Execute reload
        print("Execute reload...")
        tn.write(b"reload"+ b"\n")
        tn.read_until("[confirm]")
        tn.write(b"\n")

        # Wait reload until prompt shows "rommon 1 >"
        print("Wait reload until prompt shows rommon 1 > ")
        tn.read_until("rommon 1 >")
        tn.write(b"boot bootflash:" + file_name.encode('ascii') + b"\n")
    
        # Wait reload until initial dialog and abort all
        initial_dialog_abort(tn)

        # Change to enable mode
        print("Change to enable mode...")
        tn.read_until(">")
        tn.write(b"enable"+ b"\n")
        tn.read_until("#")

        # Change to configuration mode and set packages.conf in config file
        print("Change to configuration mode and set packages.conf in config file...")
        tn.write(b"conf t"+ b"\n")
        tn.read_until("(config)#")
        tn.write(b"boot system bootflash:packages.conf"+ b"\n")
        tn.read_until("(config)#")
        tn.write(b"end"+ b"\n")
        tn.read_until("#")

        # Save config to startup-config
        print("Save config to startup-config...")
        tn.write(b"write memory"+ b"\n")
        tn.read_until("#")

        # Install add activate commit
        print("Change to configration mode...")
        tn.write(b"install add file bootflash:" + file_name.encode('ascii') + b" activate commit"+ b"\n")

        # Confirm reload and change boot to install mode
        print("Confirm reload and change boot method to install-mode...")
        tn.read_until("This operation may require a reload of the system. Do you want to proceed? [y/n]")
        tn.write(b"y"+ b"\n")

        # Wait reload until initial dialog and abort all
        print("Wait reload until initial dialog and abort all...")
        initial_dialog_abort(tn)
        
    except EOFError:
        print("Connection closed by EOFError...")



