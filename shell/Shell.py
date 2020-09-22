#! /usr/bin/env python3
import os, sys, re
from aifc import Error

class NoArgumentsError(Error):
    pass
class TooManyArgumentsError(Error):
    pass

def redirect_in(cmd):
    pid = os.getpid()
    return_code = os.fork()
    if return_code < 0:
        os.write(2, ("Failed to fork, returning").encode())
        sys.exit(1)
    elif return_code == 0:
        os.close(0)
        os.open(cmd[cmd.index('<')+1], os.O_RDONLY)
        os.set_inheritable(0,True)
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass
        os.write(1, ("Could not run: %s\n" % cmd[0]).encode())
        sys.exit(0)
    else:
        child_pid = os.wait()
        
def redirect_out(cmd):
    pid = os.getpid()
    return_code = os.fork()
    if return_code < 0:
        os.write(2, ("Failed to fork, returning with return code: %d\n" % return_code).encode())
        sys.exit(1)
    elif return_code == 0:
        os.close(1)
        os.open(cmd[cmd.index('>')-1], os.O_CREAT | os.O_WRONLY)
        os.set_inheritable(1,True)
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir,cmd[0])
            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass
        os.write(1, ("Could not run: %s\n" % cmd[0]).encode())
        sys.exit(0)
    else:
        child_pid = os.wait()
        
def pipe(arg):
    pid = os.getpid()
    pipe = arg.index('|')
    pr, pw = os.pipe()
    for fd in (pr, pw):
        os.set_inheritable(fd,True)
    return_code = os.fork()
    if return_code < 0:
        os.write(2,("Failed to fork, returning with return code: %d\n" % return_code).encode())
        sys.exit(1)
    elif return_code == 0:
        arg = arg[:pipe]
        os.close(1)
        fd = os.dup(pw)
        os.set_inheritable(fd,True)
        for fd in (pr, pw):
            os.close(fd)
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, arg[0])
            try:
                os.execve(prog, arg, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("Could not run: %s\n" % args[0]).encode())
        sys.exit(0)
    else:
        arg = arg[pipe + 1:]
        os.close(0)
        fd = os.dup(pr)
        os.set_inheritable(fd, True)
        for fd in (pw, pr):
            os.close(fd)
        if os.path.isfile(arg[0]):
            try:
                os.execve(arg[0], arg, os.environ)
            except FileNotFoundError:
                pass
        else:
            for dir in re.split(":", os.environ['PATH']):
                prog = "%s/%s" % (dir,arg[0])
                try:
                    os.execve(prog, arg, os.environ)
                except FileNotFoundError:
                    pass
            os.write(2, ("%s isn't a recognized command" % args[0]).encode())
            sys.exit(1)

def run(cmd):
    pid = os.getpid()
    return_code = os.fork()
    if return_code < 0:
        os.write(2,("Failed to fork, returning with return code: %d\n" + return_code).encode())
        sys.exit(1)
    elif return_code == 0:
        for dir in re.split(":", os.environ['PATH']):
            prog = "%s/%s" % (dir, cmd[0])
            try:
                os.execve(prog, cmd, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("If '%s' is not a typo, use:\n     cnf %s\n" % (cmd[0],cmd[0])).encode())
        sys.exit(0)
    else:
        child_pid = os.wait()

def input_handler(cmd):
    if len(cmd) == 0: ##If cmd is empty, continue with prompt
        return
    elif cmd[0] == "quit": ##Quit shell
        sys.exit(0)
    elif "<" in cmd: ##Redirect input
        redirect_in(cmd)
    elif ">" in cmd: ##Redirect output
        redirect_out(cmd)
    elif "|" in cmd: ##Pipe command
        pipe(cmd)
    elif cmd[0] == "cd": ##Change working directory
        try:
            if len(cmd) < 2:
                raise NoArgumentsError
            elif len(cmd) > 2:
                raise TooManyArgumentsError
            else:
                os.chdir(cmd[1])
        except NoArgumentsError:
            os.write(2,"No Directory Entered\n".encode())
        except TooManyArgumentsError:
            os.write(2,"Too Many Arguments Entered\n".encode())
        except FileNotFoundError:
            os.write(2,("Directory/File: %s not found\n" % cmd[1].encode()))
    else: ##Continue with entered command
        return_code = os.fork()
        wait = True
        if "&" in cmd: ##Check for background operations
            cmd.remove("&")
            wait = False
        if return_code < 0:
            sys.exit(1)
        elif return_code == 0:
            run(cmd)
            sys.exit(0)
        else:
            if wait:
                result = os.wait()
                if result[1] != 0 and result[1] != 256:
                     os.write(2,("Program terminated with exit code: %d\n"%result[1]).encode())

def get_args(): ##Read in command arguments from os
    args = os.read(0,128)
    return args

def shell(): ##Shell control
    while True:
        prompt = "$ "
        if "PS1" in os.environ:
            prompt = os.environ["PS1"]
        os.write(1,prompt.encode())
        cmd = get_args()
        if len(cmd) == 0:
            break
        cmd = cmd.decode().split("\n")
        if not cmd:
            continue
        for c in cmd:
            input_handler(c.split())

if __name__ == "__main__":
    shell()
