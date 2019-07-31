#coding=utf-8

import re
import os
import sys

indx=0

def show():
    tmp=0
    with open('tags.txt','r') as f:
        cnt =f.readline()
        while cnt:
            tmp=tmp+1
            print(str(tmp)+' : '+cnt)
            cnt =f.readline()

def if_done():
    global indx
    indx=0
    with open('tags.txt','r') as f:
        cnt =f.readline()
        while cnt:
            indx =indx+1
            cnt =f.readline()

def chck():
    if_done()
    i=0
    for i in range(1,indx):
        if os.path.isfile(str(i)+'.txt') ==False:
            break
    return i

if __name__ =='__main__' :
    print(chck())