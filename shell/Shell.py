#! /usr/bin/env python3
import os, sys, re, time

def redirect_in(cmd):
    file_index = cmd.index('<') - 1
    file_name = cmd[file_index]
    print(file_name)
    cmd_index = cmd.index('<') + 1
    args = cmd[cmd_index:]
    print(args)

    return_code = os.fork()
    if return_code < 0:
        os.write(2, ("Failed to fork, returning").encode())
        sys.exit(1)
    elif return_code == 0:
        os.close(1)
        sys.stdout = open(file_name,"w")
        os.set_inheritable(1,True)
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, args[0])
            try:
                os.execve(prog, args, os.environ)
            except FileNotFoundError:
                pass
        os.write(1, ("Could not run: %s\n" % args[0]).encode())
        sys.exit(0)

def redirect_out(cmd):
    file_index = cmd.index('>') + 1
    cmd_index = cmd.index('>')
    file_name = cmd[file_index]
    args = cmd[:cmd_index]
    return_code = os.fork()
    if return_code < 0:
        os.write(2, ("Failed to fork, returning").encode())
        sys.exit(1)
    elif return_code == 0:
        os.close(1)
        sys.stdout = open(file_name,'w')
        os.set_inhertiable(1,True)

        for dir in re.split(":", os.environ['PATH']):
            program = "%s/%s" % (dir,args[0])
            try:
                os.execve(prog, args, os.environ)
            except FileNotFoundError:
                pass
        os.write(1, ("Could not run: %s\n" %s args[0]).encode())
        sys.exit(0)

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
        
print("Please enter a command. 'quit' exits the shell.") 


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
