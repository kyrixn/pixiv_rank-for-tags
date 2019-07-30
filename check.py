#coding=utf-8

import re
import os
import sys

indx=0

def if_done():
    global indx
    with open('tags.txt','r') as f:
        cnt =f.readline()
        while cnt:
            indx =indx+1
            print(str(indx)+' : '+cnt)
            cnt =f.readline()
    ret =os.path.isfile(str(indx)+'.txt')
    return ret

def check()

if __name__ =='__main__' :
    print(if_done())