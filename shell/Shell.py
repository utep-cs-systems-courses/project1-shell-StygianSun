#! /usr/bin/env python3
import os, sys, re, time

def check_command(cmd):
    command = re.findall('[#:|]', command)
    if command:
        return True
    else:
        return False

print("Please enter a command. 'help' returns command formatting help. 'quit' exits the shell.") 

while True:
    cmd = input("$ ")

    if check_command(cmd):
        os.write(1,("Oh, so we're piping now? I don't think so...\n").encode())
    elif cmd == "quit":
        print("Quitting. Thank you!")
        sys.exit(0)
    elif cmd == "help":
        print("\tCommand Format: [cmd][arg]\n\tQuit: 'quit'")
    elif cmd == 'redirect':
        cmd = input("$ ")
        return_codec = os.fork()
        if return_code < 0:
            os.write(2,("Fork failed. Returning %d\n" % return_code).encode())
            sys.exit(1)
        elif return_code is 0:
            args = cmd.split()
            os.close(1)
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
