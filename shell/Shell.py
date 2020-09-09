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
        return_code = os.fork()
        if return_code < 0:
            os.write(2,("Fork failed. Returning %d\n" % return_code).encode())
            sys.exit(1)
        elif return_code is 0:
            args = cmd.split()
            for dir in re.split(":", os.environ['PATH']):
                prog = "%s%s" % (dir,args[0])
                os.write(1,("Child is working... Please hold...\n").encode())
                try:
                    os.execve(prog,args,os.environ)
                    break
                except FileNotFoundError:
                    pass

            os.write(1, ("Child could not execute %s\n" % args[0]).encode())
            sys.exit(1)

        else:
            time.sleep(1)
            print("Child is done, returning to parent")
