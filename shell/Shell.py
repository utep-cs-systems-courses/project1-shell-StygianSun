#! /usr/bin/env python3
import os, sys, re, time

def check_command(cmd):
    command = cmd.split()
    if len(part) > 2:
        print("cmd check false")
        return False
    else:
        print("cmd check true")
        return True

run = True
print("Please enter a command. 'help' returns command formatting help. 'quit' exits the program.") 

while run:
    cmd = input("$ ")
    if cmd == "quit":
        print("Quitting. Thank you!")
        sys.exit(1)
    elif cmd == "help":
        print("\tFormat: [cmd][arg]\n\tquit: 'quit'")
    else:
        print("Fork go here")
