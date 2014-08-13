#!/usr/bin/python
# -*- coding: utf-8 -*-

# Non class version
# This can be used to break a line into words suitable for this assignment.

import shlex
import os
import sys
#import readline


global dictCounter
dictCounter=1
dict={}

def word_list(line):
    """Break the line into shell words.
    """

    lexer = shlex.shlex(line, posix=True)
    lexer.whitespace_split = False
    lexer.wordchars += '#$+-,./?@^='
    args = list(lexer)
    return args




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

#rest_command
def rest_command(command):
    try:
        child = os.fork()#make a child process
        if child==0:#if it is a child
            os.execvp(command[0], command)#execute command
        else:    
            os.waitpid(child,0)#wait util finished
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise



#execute commands
def exec_command(command,dict):
    try:
        if command[0] == 'history' or command[0] == 'h':
            history(command,dict)
        elif command[0] == 'pwd':
            pwd()
        elif command[0] == 'quit' or command[0] == 'q':
            quit()
        elif command[0] == 'cd':
            cd(command)
        else:
            rest_command(command)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


# history command
#def hist(command):
def history(command,dict):
    new_command=[]
    if(len(command)>1):
        #print(dict)
        print(dict.get(int(command[1])))
        new_command.append(str(dict.get(int(command[1]))))
        print(new_command)
        exec_command(new_command,dict)
    else:     
        for i in range(len(dict)):
            dict_list=str(i+1)+": "+str(dict.get(i+1))
            print(dict_list)
                
        
        
        
while True:
    line = input('psh> ')
    
    _command = word_list(line)
    dict.update({dictCounter : " ".join(_command)})
    last_command = _command[len(_command) - 1]
    exec_command(_command,dict)
    #print(dict)
    #print(len(dict))
    dictCounter+=1
   
