#! /usr/bin/env python3
import os, sys, re, time

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
        os.write(2, ("Failed to fork, returning").encode())
        sys.exit(1)
    elif return_code == 0:
        os.close(1)
        os.open(cmd[cmd.index('>')+1], os.O_CREAT | os.O_WRONLY)
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
        os.write(2,("Failed to fork").encode())
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
    cmd = cmd.split()
    if 'quit' in cmd:
        sys.exit(1)
    elif not cmd:
        pass
    elif '<' in cmd:
        redirect_in(cmd)
    elif '>' in cmd:
        redirect_out(cmd)
    elif '|' in cmd:
        pipe(cmd)
    elif '&' in cmd:
        cmd.remove("&")
        wait = False
    elif 'cd' in cmd:
        directory = cmd[1]
        try:
            os.chdir(directory)
        except FileNotFoundError:
            os.write(2,("File: %s not found" % directory).encode())
    else:
        run(cmd)

while True:
    if 'PS1' in os.environ:
        os.write(1,(os.environ['PS1']).encode())
    else:
        os.write(1,("$ ").encode())
    try:
        cmd = input()
    except EOFError:
        sys.exit(1)
    except ValueError:
        sys.exit(1)

    input_handler(cmd)
