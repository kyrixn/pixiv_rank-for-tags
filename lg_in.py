#coding:utf-8

from bs4 import BeautifulSoup
import requests
import json
import re

main_url ="https://www.pixiv.net"
log_in_url ='https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index'
post_url ='https://accounts.pixiv.net/api/login?lang=zh'

headers ={
    "User-Agent":'',
    'Referer': ''
}
dats ={
    'pixiv_id' :'',
    'password' :'',
    'post_key' :'',
    'source':'pc',
    'return_to' :'https://www.pixiv.net/'
}

ssion =requests.session()
ssion.headers =headers

def get_key():
    global dats
    doc =ssion.get(log_in_url, headers=headers)
    doc =str(doc.content,'utf-8')
    sp =BeautifulSoup(doc, 'lxml')

    targ =str(sp.find('input'))[44:-3]
    dats['post_key'] =targ
    print("---------Present key---------- : "+dats['post_key'])
    return

def login():
    pid ='';pwd =''

    mark =ret =os.path.isfile('account.txt')
    if mark:
        with open('account.txt', 'r') as f:
            pid =f.readline()
            pwd =f.readline()
    else :
        pid =input('please enter your pid :  ')
        pwd =getpass.getpass('please enter your password :  ')

        with open('accoiunt.txt','w') as f:
            f.write(pid+'\n');f.write(pwd)

    dats['pixiv_id']=pid
    dats['password']=pwd
    get_key()
    ret =ssion.post(post_url, data =dats)
    print(ret.json())
    jsn =re.search("\"body\": {\".*\"",json.dumps(ret.json())).group()[10]

    if jsn != 's':
        print("ERROR!")
        e=input("Press any key")
        exit(0)
    else:
        print('\nLogin Successfully!\n\n---------------------------------------\n')
    return ssion

if __name__ =='__main__':
    login()