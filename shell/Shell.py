#! /usr/bin/env python3
import os, sys, re, time

def redirect_in(cmd):
    print("Redirect in goes here")

def redirect_out(cmd):
    print("Redirect out goes here")

def pipe(cmd):
    print("Pipe goes here")

def run(cmd):
    return_code = os.fork()
    if return_code < 0:
        os.write(2,("Failed to fork").encode())
        sys.exit(1)
    elif return_code == 0:
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("%s isn't a recognized command\n" % cmd[0]).encode())
        sys.exit(0)
        
print("Please enter a command. 'help' returns command formatting help. 'quit' exits the shell.") 


##Main runtime loop
while True:
    print("$", end=" ")
    if 'PS1' in os.environ:
        os.write(1, os.environ['PS1'].encode())
    try:
        user_input = input()
    except EOFError:
        sys.exit(1)
    except ValueError:
        sys.exit(1)
    cmd = user_input.split()

    if not cmd: ##If entry is blank, prompts for user input
        print("Please enter a command")
    elif "quit" in cmd: ##Exits primary shell
        sys.exit(0)
    elif "<" in cmd: ## Check for an input redirect
        redirect_in(cmd)
    elif ">" in cmd: ## Check for an output redirect
        redirect_out(cmd)
    elif "|" in cmd: ## Check for pipe command
        pipe(cmd)
    else: ## Runs any remaining valid command
        run(cmd)
