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

while run:
    cmd = input("$ ")
    if cmd == "quit":
        print("quitting")
        sys.exit(1)
    elif cmd == "help":
        print("help message")
    else:
        print("Fork go here")
