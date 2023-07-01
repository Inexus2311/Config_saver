# Imports
import platform
import getpass
import sys
import os
import argparse

"# import paramiko"
import colorama
from colorama import Fore
from colorama import Fore, Style


username = None
password = None

# Menu mode
# mode = ""

# **************************************************#
# Functions
# **************************************************#


# **************************************************#
# Print Message Function
# **************************************************#
def print_colored_message(message, color):
    print(f"{color}{message}{Style.RESET_ALL}")


# **************************************************#
# Failed checking Input close Program
# **************************************************#


def Close():
    print("Program occurs an error! Closing Program now!")
    sys.exit()


# **************************************************#
# Check bad input characters
# **************************************************#


def bad_input(user_input):
    # define set of invalid characters
    bad_chars = {"&", "|", ";", "$", ">", "<", "\\", "!", "'", "--", "-"}
    # check if_user input contains only valid characters
    if any(c in bad_chars for c in user_input):
        return True
    else:
        return False


# **************************************************#
# Check the input routine
# **************************************************#


def check_input_valid(input):
    if input is not None:
        if bad_input(input):
            print(f"Input: {input} contains invalid characters!")
            input = "None"
            Close()
        else:
            return input
    else:
        return input


# **************************************************#
# Update save Directory and filename of switch_List
# **************************************************#


def change_values(arg1, arg2):
    while not os.path.exists(arg1):
        print_colored_message(
            "[INFO] Der Pfad: {0} ist nicht vorhanden.".format(arg1), Fore.RED
        )
        str1 = "Geben Sie einen gültigen Pfad ein \
oder beenden Sie das Programm mit Q : "

        user_input = input(str1)
        if Quit(user_input):
            pass
        else:
            arg1 = user_input

    while not os.path.exists(arg2):
        # os.system("clear")
        str2 = "Geben Sie eine gültige Datei ein \
oder beenden Sie das Programm mit Q : "
        user_input = input(str2)
        if Quit(user_input):
            pass
        else:
            arg2 = user_input
            print_colored_message(
                "[INFO][+] Die Datei: {0} ist vorhanden.".format(arg2), Fore.Green
            )
    return [arg1, arg2]


# **************************************************#
# Close Programm
# **************************************************#


def Quit(arg1):
    if arg1.lower() == "q":
        print("Closing Program immediately! ")
        sys.exit()
    else:
        return 0


# **************************************************#
# Check input_answer
# **************************************************#
# function check_input check input if it is Y or N then return true else return false


def check_input(input_answer):
    if input_answer is not None:
        if input_answer.lower() == "y":
            return True
        elif input_answer.lower() == "n":
            return False
        else:
            return False


# **************************************************#
# Check if a file can be reading
# **************************************************#


def check_reading(file_name):
    try:
        file = open(file_name, "r")
        print_colored_message(
            f"[Info][+]... Reading file '{file_name}' was successfully", Fore.BLUE
        )
        file.close()
    except file.errors:
        print_colored_message("[-] Die Datei konnte nicht geöffnet werden.", Fore.RED)
        os.exit()


# **************************************************#
# SCP-Connection routine
# **************************************************#


def scp_authenticated(zpath, file_name):
    global username, password
    if username is None or password is None:
        username = input("Geben Sie Ihren TACAS-Username ein!: ")
        password = getpass.getpass("Bitte geben Sie Ihr Passwort ein!: ")
    # password = input("Bitte geben Sie Ihr Passwort ein!: ")
    """
    #Connection Details
    for line in file_list:
        hostname = line.strip()
        #Create a SSH client
        client = paramiko.SSHClient()
        # Make sure that we add the remote server's SSH key automatically
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Connect to the client
        try:
            client.connect(hostname,username=username,password=password)
            print("SSH session to %s is open" %hostname)
            break
        except client.error:
            print("[-] Authentifizierung fehlgeschlagen!")
            break
    """
    if username == "" or password == "":
        return 0

    with open(file_name, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                print_colored_message(
                    "[-] Keine Liste in File enthalten! \
Vorgang wird abgebrochen!",
                    Fore.RED,
                )
                sys.exit()
            else:
                if line.isalpha() and len(line) >= 0:
                    print_colored_message(
                        "[-] Leere Zeile in File enthalten! \
Vorgang wird abgebrochen!",
                        Fore.RED,
                    )
                    sys.exit()
                else:
                    switch_name = line.strip()
                    system = platform.system()
                    target_file_name = "running-config"
                    if "/" in zpath:
                        file = zpath + switch_name
                    else:
                        file = zpath + "/" + switch_name
                    if system == "Linux":
                        command = f"sshpass -p {password} scp \
        {username}@{switch_name}:{target_file_name} {file}_test.txt"
                        cmd = (
                            f"sshpass -p {password} \
        ssh {username}@{switch_name}"
                            + " dir "
                            + "%s" % (target_file_name)
                        )
                    elif system == "Windows":
                        command = f"scp {username}@{switch_name}:{target_file_name} {file}_test.txt"
                        # cmd = f"scp {username}@{switch_name}:%s {switch_name}_test.txt" % (
                        #    target_file_name)
                        # Execute command to check the presence of file
                        cmd = (
                            "ssh "
                            + username
                            + "@"
                            + switch_name
                            + " dir "
                            + target_file_name
                        )
                    else:
                        print_colored_message("Unbekanntes Betriebssystem", Fore.YELLOW)
                try:
                    # Check target_file is available on the system
                    input_answer = input(
                        "Do you want to check the running-config on the target system? (Y/N): "
                    )
                    while check_File_input(input_answer):
                        input_answer = input("[-] Falsche Eingabe! (Y/N): ")
                    if input_answer.lower() == "y":
                        # Check if target file is available
                        if os.system(cmd):
                            raise OSError("[-] Keine Zieldatei vorhanden")
                        else:
                            print_colored_message(
                                f"[+] Die Datei {target_file_name} existiert!",
                                Fore.GREEN,
                            )
                    else:
                        print_colored_message(
                            "[-] Checking running-config on target system was skipped!",
                            Fore.BLUE,
                        )
                except OSError:
                    print_colored_message(
                        f"[Info][-] Die Datei {target_file_name} existiert \
nicht auf dem Zielhost!",
                        Fore.RED,
                    )
                    input_answer = ""
                    print_colored_message(
                        "[Info][-] Running-config on target system was not found !",
                        Fore.RED,
                    )
                    while check_File_input(input_answer):
                        input_answer = input(
                            "[-] Command failed! Do you want to contiune ? (Y/N): "
                        )
                    if input_answer.lower() == "y":
                        continue
                    else:
                        print_colored_message(
                            "[Info][-] Command failed to excecute!", Fore.RED
                        )
                        sys.exit()
                try:
                    input_answer = input(
                        "Should be create a switch test config on your Folder? (Y/N): "
                    )
                    # while checking the input_answer until your input_answer is  Y or N
                    while check_File_input(input_answer):
                        input_answer = input("[-] Falsche Eingabe! (Y/N): ")
                    if input_answer.lower() == "y":
                        # os.system('echo ' + password + ' | ' + command)
                        if os.system(command) != 0:
                            raise Exception("[-] SSH Authentication failed!")
                        else:
                            print_colored_message(
                                "[+] SSH Connection passed", Fore.GREEN
                            )
                            test_create_config(zpath, switch_name)
                            break
                    else:
                        print_colored_message(
                            f"[-] Switch test config was skipped!", Fore.BLUE
                        )
                        break

                except Exception:
                    print_colored_message(
                        "[-] SSH Connection Authentication failed!", Fore.RED
                    )
                    print_colored_message("[-] Command failed to excecute", Fore.RED)
                    input_answer = ""
                    while check_File_input(input_answer):
                        input_answer = input(
                            "[-] Command failed! Do you want to contiune ? Y/N:  "
                        )
                    if input_answer.lower() == "y":
                        continue
                    else:
                        print_colored_message(
                            "[-] Command failed to excecute!", Fore.RED
                        )
                        sys.exit()
                    sys.exit()

    return [username, password]


# **************************************************#
# Create test config file
# **************************************************#


def test_create_config(zpath, switch_name):
    print("Creating test config file")
    file = ""
    if "/" in zpath:
        file = zpath + switch_name
    else:
        file = zpath + "/" + switch_name
    if os.path.isfile(f"{switch_name}_test.txt"):
        print_colored_message(
            f"[INFO][+] Die Testdatei {switch_name}_test.txt \ist bereits vorhanden!",
            Fore.GREEN,
        )
    else:
        print_colored_message(
            f"[+] Testfile: {switch_name}_test.txt \
was created!",
            Fore.GREEN,
        )
        ans = input(
            f"[INFO?] Soll die Datei {switch_name}_test.txt \
gelöscht werden? Y/N: "
        )
        while check_File_input(ans):
            ans = input(
                "[-] Falsche Eingabe!\n"
                f"Soll die Datei \
                        {switch_name}_test.txt gelöscht werden? Y/N: "
            )
        if ans.lower() == "y":
            if "/" in zpath:
                file_save = file + "_test.txt"
            else:
                file_save = file + "_test.txt"
                if os.path.isfile(file_save):
                    os.remove(file_save)
                    print_colored_message(f"File: {file_save} is deleted!", Fore.GREEN)
                else:
                    print_colored_message("[-] File not found!", Fore.RED)
        elif ans.lower() == "n":
            pass


# **************************************************#
# Save Config file from Switch
# **************************************************#


def config_save(zpath, file):
    # Check SSH Connection
    print("Checking the SCP Connection.....")
    target_file_name = "running-config"
    creds = scp_authenticated(zpath, file)
    if creds == 0:
        sys.exit()

    file_name = file
    with open(file_name, "r") as f:
        for line in f:
            # print(f"{line}", end="")
            switch_name = line.strip()
            if "/" in zpath:
                file = zpath + switch_name + ".txt"
            else:
                file = zpath + "/" + switch_name + ".txt"
            # print(switch_name)
            if switch_name:
                system = platform.system()
                if system == "Windows":
                    command = (
                        f"scp -q {creds[0]}@{switch_name}:{target_file_name} {file}"
                    )
                if system == "Linux":
                    command = f"sshpass -p {creds[1]} scp -q {creds[0]}@{switch_name}:{target_file_name} {file}"
                """ command = (
                    f"sshpass -p {creds[1]} scp -q \
{creds[0]}@{switch_name}:{target_file_name}  {zpath}/{file_name}.txt"
                    """
                # {file}.txt"
                if os.path.isfile(f"{file}"):
                    print_colored_message(
                        f"[+] {switch_name}.txt bereits vorhanden!", Fore.YELLOW
                    )
                    continue
                else:
                    print_colored_message(
                        f"[Info][!] Starting Saving on Switch: {switch_name}",
                        Fore.YELLOW,
                    )
                    try:
                        if os.system(command) != 0:
                            raise Exception("[-] Wrong Command does not exist")
                    # print(subprocess.check_output(os.system(command),shell=True)
                    except Exception:
                        print("[-] Command couldn't excecute")
                        sys.exit()

                    if os.path.isfile(f"{file}"):
                        print_colored_message(
                            f"[INFO][+] Die Datei {switch_name}.txt \
wurde erfolgreich heruntergeladen!",
                            Fore.GREEN,
                        )
                    else:
                        print_colored_message(
                            f"[INFO][-] Die Datei {switch_name}.txt \
konnte nicht heruntergeladen werden!",
                            Fore.RED,
                        )
                        break
            else:
                continue


# **************************************************#
# Check arguments are valid
# **************************************************#


def check_arguments(arg1, arg2, state_print=True):
    if state_print:
        state_print = False
        print("\n")
        print("# ************************************************** #" + "\n")
        print("Überprüfung folgender Eingabe:\n")
        print("[+] Zielpfad: {0}\n[+] Filename: {1}\n".format(arg1, arg2))
        print("# ************************************************** #")
        print("\n")
    check = False

    # Check if Path is available
    if not os.path.exists(arg1):
        return check
    # Check if File is available
    if not os.path.isfile(arg2):
        return check
    check = True
    state_print = True

    print_colored_message(
        "[INFO][+] Der Pfad: '{0}' ist vorhanden.".format(arg1), Fore.GREEN
    )
    print_colored_message(
        "[INFO][+] Die Datei: '{0}' ist vorhanden.".format(arg2), Fore.GREEN
    )

    return check


# **************************************************#
# Print Message to finish script
# **************************************************#


def finish():
    print_colored_message(f"[INFO][+] All Savings are done!", Fore.YELLOW)
    sys.exit()
    exit()


# **************************************************#
# Default Config Mode routine
# **************************************************#


def default_mode(zpath, file):
    # Check your valid arguments
    if check_arguments(zpath, file):
        check_reading(file)
        print("Starting saving Configs from Switch:")
        config_save(zpath, file)
        finish()
    else:
        while not check_arguments(zpath, file, state_print=False):
            string = change_values(zpath, file)
            zpath = string[0]
            file = string[1]

        check_reading(file)
        print("Starting saving Configs from Switch:")
        config_save(zpath, file)
        finish()


# **************************************************#
# Argument Config Mode routine
# **************************************************#


def argument_mode(arg1, arg2):
    if check_arguments(arg1, arg2):
        check_reading(arg2)
        print("Starting saving Configs from Switch:")
        config_save(arg1, arg2)
        finish()
    else:
        string = change_values(arg1, arg2)
        arg1 = string[0]
        arg2 = string[1]
        check_reading(arg2)
        print("Starting saving Configs from Switch:")
        config_save(arg1, arg2)
        finish()


# **************************************************#
# Helper-Menue
# **************************************************#


def Menu(argv):
    print(f"usage: {argv[0]} [-sd save director] [-sw_list Switch_liste]")
    print_colored_message(
        f"Example: python3 {argv[0]} -sd C:/user/path -sw_list test_file.txt", Fore.BLUE
    )
    print()


def print_colored_usage(argv):
    print(
        f"{Fore.YELLOW}usage: {argv[0]} {Fore.CYAN}[-sd save director] {Fore.CYAN}[-sw_list Switch_liste]{Fore.RESET}"
    )
    print(
        f"{Fore.GREEN}Example: python3 {argv[0]} {Fore.CYAN}-sd C:/user/path {Fore.CYAN}-sw_list test_file.txt{Fore.RESET}"
    )
    print()


# **************************************************#
# Parser
# **************************************************#


def parse_args():
    parser = argparse.ArgumentParser(description="Description of your program")
    parser.add_argument("-sd", "--save_director", help="save_directory")
    parser.add_argument("-sw_list", "--switch_list", help="list of switch")
    args = parser.parse_args()
    return args


# **************************************************#
# Check File input routine
# **************************************************#


def check_File_input(ans):
    if ans.lower() == "y":
        return False
    elif ans.lower() == "n":
        return False
    else:
        return True
