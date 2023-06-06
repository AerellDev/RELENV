import os

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def open_new_cmd_and_execute_command(command):
    os.system(f'start cmd /k "{command}"')