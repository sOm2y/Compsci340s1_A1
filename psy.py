#Author: Yue Yin
#UPI: yyin888
#ID: 5398177

#!/usr/bin/python
# -*- coding: utf-8 -*-

# Non class version
# This can be used to break a line into words suitable for this assignment.

import shlex
import os
import sys
import subprocess
#import readline

#global variable
global dictCounter
dictCounter=1
global job_counter
job_counter=1
global _vaildCommand
_vaildCommand=True
dict={}
jobList={}
state=[]



#read input
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



#change filepath
def cd(command):
    try:
        _curPath = os.getcwd()
        if len(command)>1:
            os.chdir(_curPath + "/" + command[1])
        else:
            print("cd: "+command[0]+": No such file or directory")
    except OSError:
        print("cd: "+command[1]+": No such file or directory")

#add job 
def add_job(command,child,job_counter):
    try:
        idCommand=[]
        idCommand[0]=child
        idCommand[1]=command
        jobList.update({job_counter : " ".join(idCommand)})
        print("["+str(job_counter)+"] "+str(child))  
    except:
         print("Unexpected error2:", sys.exc_info())

#rest_command
def rest_command(command,job_counter,_vaildCommand):
    try:
        ampersand='&' in command
        if ampersand:
            del command[len(command)-1]
        child = os.fork()#make a child process
        if child==0:#if it is a child
            os.execvp(command[0], command)#execute command
        else:
            if ampersand:
                add_job(command,child,job_counter)
            else:    
                os.waitpid(child,0)#wait util finished
    except:
#        _vaildCommand=False
#        print(_vaildCommand)
        print("Command doesn't exsit!")
        



# history command
#def hist(command):
def history(command,dict):
    new_command=[]
    if(len(command)>1):
        #print(dict)
        print(dict.get(int(command[1])))
        
        new_command=str(dict.get(int(command[1]))).split()
        print(new_command)
        exec_command(new_command,dict,job_counter)
    else:     
        if(len(dict)>10):
            for i in range((len(dict)-10),len(dict)):
                dict_list=str(i+1)+": "+str(dict.get(i+1))
                print(dict_list)
        else:
            for i in range(len(dict)):
                dict_list=str(i+1)+": "+str(dict.get(i+1))
                print(dict_list)
    


#check "|" in right position
def checkPipe(command):
    if command[0] == '|' or command[len(command)-1]=='|':
        print("Invalid use of pipe '|'. ")
        #print(command)
        return False
    else:
        for i in range( 1,len(command)-1):
            if command[i]=='|' and command[i+1]=='|':
                print("Invalid use of pipe '|'.")
                return False
    #print("correct pipeline input")
    return True
            
            
#pipeline
def pipeline(command):
    
        try:      
            if '&' in command:
                amper=1
            else:
                amper=0
                
            #child process
            child=os.fork()
            if child==0 :
                while '|' in command:
                    #get '|' index position    
                    pipe_index=command.index('|')
                    r,w=os.pipe()
                    grand_child=os.fork()
                    if grand_child==0:
                        os.dup2(w,1)#replace to w in index 1
                        os.close(w)#close w
                        os.close(r)# close stand in 
                        os.execvp(command[0],command[0:pipe_index])# execute command before '|'
                    os.dup2(r,0)
                    os.close(r)
                    os.close(w)
                    del command[:pipe_index+1]
                os.execvp(command[0],command)
            else:
                if amper==0:
                    os.waitpid(child,0)
        except:
            print("Unexpected error2:", sys.exc_info()[0])


#jobs
def jobs(jobList):
    for jobKey in jobList.keys():
        pid=jobList[jobKey]
        ps=subprocess.Popen(['ps','-p',str(pid),'-o','state='],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        result,error=ps.communicate()
        if result.decode()!='':
            print('[{}] <{}> {}'.format(jobKey,result.decode()[0],str(pid)))
            #print("jobs")
            
#execute commands            
def exec_command(command,dict,job_counter):
    try:
#        last_command = _command[len(_command) - 1]
        if command[0] == 'history' or command[0] == 'h':
            history(command,dict)
        elif command[0] == 'pwd':
            pwd()
        elif command[0] == 'cd':
            cd(command)
        elif '|' in command:
            if checkPipe(command):
                pipeline(command)
                #print("pipe")
        elif command[0]=='jobs':
            jobs(jobList);
        else:
            rest_command(command,job_counter,_vaildCommand)
    except:
        print("Unexpected error1:", sys.exc_info())
        

    
    
        
while True:
    try:
        line = input('psh> ')
    except EOFError:
        break
    _command = word_list(line)
    
    exec_command(_command,dict,job_counter)
    if _vaildCommand:
        dict.update({dictCounter : " ".join(_command)})
    #print(dict)
    #print(len(dict))
    dictCounter+=1
    job_counter+=1
   
