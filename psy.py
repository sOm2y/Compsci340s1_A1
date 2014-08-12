#!/usr/bin/python
# -*- coding: utf-8 -*-

# Non class version
# This can be used to break a line into words suitable for this assignment.

import shlex
import os
import sys
#import readline


dictCounter=0

def word_list(line):
    """Break the line into shell words.
    """

    lexer = shlex.shlex(line, posix=True)
    lexer.whitespace_split = False
    lexer.wordchars += '#$+-,./?@^='
    args = list(lexer)
    return args


# history command
#def hist(command):
    
    


def history(command):
    if(len(command)>1):
        print ("1")
    else:     
        print ("2")
        

#print current path
def pwd():
    print (os.getcwd())

#exit tool
def quit():
    sys.exit()

#change filepath
def cd(command):
    try:
        _curPath = os.getcwd()
        os.chdir(_curPath + "/" + command[1])
    except OSError:
        print("cd: "+command[1]+": No such file or directory")

#srest_command
def rest_command(command):
    child = os.fork()#make a child process
    if child==0:#if it is a child
        os.execvp(command[0], command)#execute command
    else:    
        os.waitpid(child,0)#wait util finished



#execute commands
def exec_command(command):
    try:
        dict={dictCounter : " ".join(command)}

        if command[0] == 'history' or command[0] == 'h':
            history(command)
        elif command[0] == 'pwd':
            pwd()
        elif command[0] == 'quit' or command[0] == 'q':
            quit()
        elif command[0] == 'cd':
            cd(command)
        else:
            rest_command(command)
    except:
        e = sys.exc_info()[0]
        write_to_page( "<p>Error: %s</p>" % e )



while True:
    line = input('psh> ')

    _command = word_list(line)
    last_command = _command[len(_command) - 1]
    try:
        exec_command(_command)
    except:
        print("Command doesn't exsit!")

