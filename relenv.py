from os import system
from art import *
from src.config import PROGRAM_NAME, PROGRAM_CREATOR, PROGRAM_VERSION
from src.utils import clear_console, open_new_cmd_and_execute_command
import json

custom_user_data = []

def init():
    clear_console()
    system("title " + PROGRAM_NAME + " - " + PROGRAM_VERSION)
    tprint(PROGRAM_NAME)
    print("Version :", PROGRAM_VERSION)
    print("Create By", PROGRAM_CREATOR, "\n")

def menu(msg = None):
    print("1. Create Custom User Data")
    print("2. List Custom User Data")
    print("3. Remove Custom User Data")
    print("4. Exit\n")
    if msg != None: print("Notif :", msg)
    answer = input("Select (1, 2, 3, 4) : ")
    try:
        answer = int(answer)
    except Exception:
        restart(str(answer) + " is not selected.")
        return False

    if answer == 1:
        create_custom_user_data()
    elif answer == 2:
        list_custom_user_data()
    elif answer == 3:
        remove_custom_user_data()
    elif answer == 4:
        exit()
    elif answer != 1 or 2 or 3 or 4:
        restart(str(answer) + " not found, please select 1, 2, 3 or 4.")

def restart(msg = None):
    init()
    menu(msg=msg)

def create_custom_user_data(pname = None, pprogram_name = None, pprogram_path = None, premote_debugging_port = None, puser_data_dir = None):
    load_custom_user_data()
    init()
    name = pname
    program_name = pprogram_name
    program_path = pprogram_path
    remote_debugging_port = premote_debugging_port
    user_data_dir = puser_data_dir

    if name != None:
        print("Name :", name)
    else:
        name = input("Name : ")

    if program_name != None:
        print("Program Name :", program_name)
    else:
        program_name = input("Program Name : ")

    if program_path != None:
        print("Program Path :", program_path)
    else:
        program_path = input("Program Path : ")

    answer = input("Custom Port? (y/n) : ")
    if answer == "y":
        remote_debugging_port = input("Custom Port : ")
    elif answer == "n":
        pass
    elif answer != "y" or "n":
        create_custom_user_data(name, program_name, program_path, remote_debugging_port, user_data_dir)
        return False
        

    if user_data_dir != None:
        print("User data path :", user_data_dir)
    else:
        user_data_dir = input("User data path : ")

    temp = {}

    if name != None : temp["name"] = name
    if program_name != None : temp["program_name"] = program_name
    if program_path != None : temp["program_path"] = program_path
    if remote_debugging_port != None : temp["remote_debugging_port"] = remote_debugging_port
    if user_data_dir != None : temp["user_data_dir"] = user_data_dir

    custom_user_data.append(temp)
    save_custom_user_data()
    restart("Add " + name + " to list.")

def load_custom_user_data():
    global custom_user_data
    with open("./data/saved.json", "r") as file:
        temp = json.load(file)
        custom_user_data = temp

def save_custom_user_data():
    with open("./data/saved.json", "w") as file :
        temp = json.dumps(custom_user_data)
        file.write(temp)

def list_custom_user_data(msg = None):
    init()
    load_custom_user_data()
    if not len(custom_user_data) > 0:
        restart("List empty.")
        return False
    print("Select what you want to load...\n")
    i = 1
    for data in custom_user_data:
        print(str(i) + ".", data["name"])
        i += 1
    back_num = i
    print(str(back_num) + ". Back\n")
    select_text = "Select ("
    for a in range(i):
        select_text += str(a + 1) + (", " if a != (i - 1) else ") : ")

    if msg != None: print("Notif :", msg)
    answer = input(select_text)
    try:
        answer = int(answer)
    except Exception:
        list_custom_user_data(str(answer) + " is not selected.")
        return False
    
    for a in range(i):
        a += 1
        if answer == a:
            run_program_with_custom_user_data(custom_user_data[a - 1]["name"], custom_user_data[a - 1]["program_name"], custom_user_data[a - 1]["program_path"], custom_user_data[a - 1]["remote_debugging_port"], custom_user_data[a - 1]["user_data_dir"])
            return False
        elif answer == back_num:
            restart()
            return False

    list_custom_user_data(str(answer) + " is not selected.")

def run_program_with_custom_user_data(name, program_name, program_path, remote_debugging_port = None, user_data_dir = None):
    command = f'title {name} & ' + (f'mkdir "{user_data_dir}" & ' if user_data_dir != None else "") + f'cd {program_path} & {program_name}' + (f" --remote-debugging-port={remote_debugging_port}" if remote_debugging_port != None else "") + f' --user-data-dir="{user_data_dir}"' if user_data_dir != None else ""
    open_new_cmd_and_execute_command(command)

def remove_custom_user_data(msg = None):
    init()
    load_custom_user_data()
    if not len(custom_user_data) > 0:
        restart("List empty.")
        return False
    print("Select what you want to delete...\n")
    i = 1
    for data in custom_user_data:
        print(str(i) + ".", data["name"])
        i += 1
    back_num = i
    print(str(back_num) + ". Back\n")
    select_text = "Select ("
    for a in range(i):
        select_text += str(a + 1) + (", " if a != (i - 1) else ") : ")

    if msg != None: print("Notif :", msg)
    answer = input(select_text)
    try:
        answer = int(answer)
    except Exception:
        remove_custom_user_data(str(answer) + " is not selected.")
        return False
    
    for a in range(i):
        a += 1
        if answer == a:
            custom_user_data.pop(a - 1)
            save_custom_user_data()
            restart("Succesfuly delete.")
            return False
        elif answer == back_num:
            restart()
            return False

    remove_custom_user_data(str(answer) + " is not selected.")

restart()