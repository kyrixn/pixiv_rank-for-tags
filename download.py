#coding=utf-8

from bs4 import BeautifulSoup
import requests
import re
import json
import os

import lg_in as lg
import check

main_url ="https://www.pixiv.net"
headers ={
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36',
    'Referer': ''
}

ssion =requests.session()
ssion.headers =headers

id_lst =['']*500

def get_id(ss):
    for i in range(1,len(ss)):
        if ss[i] == ':':
            return ss[0:i-1]

def change_url(ss, iid):
    url ='https://i.pximg.net/img-original/img/'+ss[65:69]+ss[70:73]+ss[74:77]+ss[78:81]+ss[82:85]+ss[86:89]+'/'+iid+'_p0.png'
    return url


if __name__ == '__main__':
    check.show()
    tag =input("Chose a tag: ")
    while int(tag) >= check.chck():
        print("Haven't done, please wait............")

    idx=0
    with open(str(tag)+'.txt','r') as f:
        now =f.readline()
        while now:
            id_lst[idx] =get_id(now)
            idx=idx+1
            now =f.readline()

    os.chdir(os.path.join(os.getcwd(), 'photos'))
    ssion =lg.login()

    for tmp in id_lst:
        print("Recent image Pid: "+tmp)
        url='https://www.pixiv.net/member_illust.php?mode=medium&illust_id='+tmp

        ret =ssion.get(url, headers =headers, timeout =(3,7))
        doc =str(ret.content, 'utf-8')
        sp =BeautifulSoup(doc, 'lxml')

        targ =sp.find("head").find_all("script")
        targ =str(targ[5])
        
        patt =re.compile(r'urls":{"mini":"https:.*\.jpg","thumb"')
        res =patt.findall(targ)[0]
        res =change_url(res, tmp)
        print(res)
            
        headers['Referer'] =url
        pic_name =tmp+'.jpg'
        source =ssion.get(res, headers =headers)
            
        if str(source.status_code)=='404':
            res =res[:-3]+'jpg'
            source =ssion.get(res, headers =headers)
        if str(source.status_code)=='200':
            with open(pic_name, "wb") as f:
                f.write(source.content)
            print(".......DONE!!!\n")
        else :
            print("#########Failed！")