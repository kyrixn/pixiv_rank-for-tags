#coding:utf-8

from bs4 import BeautifulSoup
import requests
import json
import re
import getpass
import sys
import os

import lg_in as lg

main_url ="https://www.pixiv.net"

headers ={
    "User-Agent":'',
    'Referer': ''
}

ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "  
            "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",  
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "  
            "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",  
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "  
            "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "  
            "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",  
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "  
            "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",  
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "  
            "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",  
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "  
            "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",  
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",  
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",  
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "  
            "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",  
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "  
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",  
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "  
            "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"  
           ] 
#19条

ssion =requests.session()
ssion.headers =headers

heap,likes,lev=[],[],[20000,10000,5000,1000,500,100]
mk =True
h,t=int(1),int(0)

# ---------------------HEAP-----------------------
def Insert(num, iid):
    print(num, iid)
    num, iid=int(num), int(iid)
    global heap,h,t,likes,mk
    t+=1
    heap[t] =iid
    likes[t] =num
    now,nxt =int(t),int(0)
    mark =True

    while mark:
        mark =False
        if now%2 ==0:
            nxt =now/2
        else:
            nxt =(now-1)/2
        if likes[int(nxt)]<likes[int(now)]:
            mark =True
            heap[int(nxt)],heap[int(now)] =heap[int(now)], heap[int(nxt)]
            likes[int(nxt)],likes[int(now)] =likes[int(now)], likes[int(nxt)]
            now =nxt
    if t>210:
        t-=1
    return

def put_out():
    global heap,h,t,likes,mk
    tg,lk =heap[1], likes[1]
    heap[1] =heap[t]
    likes[1] =likes[t]
    t-=1
    if t==0:
        mk =False
        return tg

    now,nxt=int(1),int(1)
    mark =True

    while mark:
        mark =False
        nxt,tmp =now*2,0
        if nxt>t:
            break
        if likes[int(nxt)]<likes[int(nxt+1)]:
            tmp =nxt+1
        else :
            tmp =nxt

        if likes[int(tmp)] >likes[int(now)]:
            mark =True
            heap[int(tmp)],heap[int(now)] = heap[int(now)],heap[int(tmp)]
            likes[int(tmp)], likes[int(now)] =likes[int(now)], likes[int(tmp)]
            now =tmp
    return str(tg)+' : '+str(lk)
# ---------------------END-------------------------

def init():
    global heap,likes,h,t,mk
    heap,likes =[int(1e9)]*250,[int(1e9)]*250
    mk =True
    h,t =int(1),int(0)
    return

def work(targ):
    p1,p2,p3,p4=re.compile('"illustId":"\d+"'), re.compile('"bookmarkCount":\d+'), re.compile('"tags":\[.{8}'), re.compile('R-\d\d')
    lt1, lt2, lt3 =p1.findall(targ), p2.findall(targ), p3.findall(targ)

    print(len(lt3))

    for i in range(0,len(lt1)):
        if len(p4.findall(lt3[i])) == 0:
            Insert(lt2[i][16:], lt1[i][12:-1])


def maintain(lv, tag):
    tmp=0
    print(lv)

    doc =ssion.get(main_url+'/search.php?s_mode=s_tag&word='+tag+'%20'+str(lv))
    sp =BeautifulSoup(str(doc.content,'utf-8'), 'lxml')
    amout =int(sp.find(class_='count-badge').text[:-1])
    print(amout)
    if amout ==0:
        return
    pg=int(min(1000, int(amout/40)+1))
    for i in range (1,pg+1):
        print(i)

        headers['Referer']=ua_list[(tmp%19)]
        tmp+=1
        doc =ssion.get(main_url+'/search.php?s_mode=s_tag&word='+tag+'%20'+str(lv)+'&order=date_d&p='+str(i), headers =headers)
        sp =BeautifulSoup(str(doc.content, 'utf-8'), 'lxml')
        targ =sp.find('input', id='js-mount-point-search-result-list').get('data-items')
        work(targ)

def get_rank(tag):
    global lev
    for lv in lev:
        maintain(lv, tag)
    return
# -------------------------main-------------------------------

ssion =lg.login()
with open('tags.txt', 'r') as f:
    tg =f.readline()
    print("Now ===> "+tg)
    indx=1
    while tg:
        init()
        get_rank(tg)
        print(likes)
        st,cur='',''
        with open(str(indx)+'.txt', 'w') as ff:
            while mk:
                cur =str(put_out())
                if cur==st:
                    continue
                st =cur
                ff.write(st+'\n')
        indx+=1

        print ('DONE!!!!!!!!!!!!!!!')
        tg =f.readline()
with open(str(indx)+'.txt', 'w') as f:
    f.write('done')
