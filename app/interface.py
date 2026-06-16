from os import name, system

def clear_screen():
    if name == "nt":
        system("cls")
    else:
        system("clear")

def print_error(text):
    print("\033[31m"+text+"\033[0m")

def print_success(text):
    print("\033[32m"+text+"\033[0m")

def print_warning(text):
    print("\033[33m"+text+"\033[0m")

def mk_error(text):
    return ("\033[31m"+text+"\033[0m")

def mk_success(text):
    return ("\033[32m"+text+"\033[0m")

def mk_warning(text):
    return ("\033[33m"+text+"\033[0m")

def mk_prompt(text):
    return ("\033[36m"+text+"\033[0m")

def mk_tags(text):
    return ("\033[2m"+text+"\033[0m")