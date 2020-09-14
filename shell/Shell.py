#! /usr/bin/env python3
import os, sys, re, time

def check_command(cmd):
    command = re.findall('[#:|]', cmd)
    if command:
        return True
    else:
        return False

print("Please enter a command. 'help' returns command formatting help. 'quit' exits the shell.") 

while True:
    cmd = input("$ ") ##Prompt user for command

    if check_command(cmd) == True: ##Checks users command input for pipe command
        os.write(1,("Oh, so we're piping now? I don't think so...\n").encode())
    elif cmd == "quit":
        print("Quitting. Thank you!")
        sys.exit(0)
    elif cmd == "help": ##Help for command formatting
        print("\tCommand Format: [cmd][arg]\n\tQuit: 'quit'")
    elif cmd == 'redirect': #Redirection
        cmd = input("$ ")
        return_code = os.fork() #Creates a child to run the process
        if return_code < 0: #If child fails
            os.write(2,("Fork failed. Returning %d\n" % return_code).encode())
            sys.exit(1)
        elif return_code is 0: #If child succeeds
            args = cmd.split()
            os.close(1) ##Redirects output to output.txt
            os.open("output.txt", os.O_WRONLY | os.O_APPEND)
            os.set_inheritable(1, True)

            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                try:
                    os.execve(program,args,os.environ)
                except FileNotFoundError:
                    pass
            os.write(2,("Child: Error. Could not exec %s\n" % args[1]).encode())
            sys.exit(0)
    else: ##If not redirecting, output goes to terminal
        return_code = os.fork()
        if return_code < 0:
            os.write(2,("Fork Failed. Returning %d\n" % rc).encode())
            sys.exit(1)
        elif return_code == 0:
            args = cmd.split()
            for dir in re.split(":", os.environ['PATH']):
                program = "%s/%s" % (dir, args[0])
                os.write(1,("Child is attempting to exec %s\n" % args[0]).encode())
                try:
                    os.execve(program, args, os.environ)
                    break
                except FileNotFoundError:
                    pass
            os.write(1, ("Child reporting in: Could not exec %s\n" % args[0]).encode())
            sys.exit(1)
