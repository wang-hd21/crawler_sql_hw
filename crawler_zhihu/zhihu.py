from typing import Any
import requests
from bs4 import BeautifulSoup as bs
import json
import time
import datetime
import pymysql
from tqdm import tqdm
def connect():
    resp = requests.get("https://www.zhihu.com/billboard",headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"})
    if 200 <= resp.status_code < 300 :
        zhihuxml = bs(resp.text,'lxml')
        data = zhihuxml.find_all(type="text/json",id="js-initialData")
        datajson = json.loads(data[0].text)
        boardlist = datajson["initialState"]["topstory"]["hotList"]
        return boardlist
    return None

def str_to_int(s:str):
    i=0
    re=0
    while i < len(s) and '0' <= s[i] <= '9'  :
        re *= 10
        re += int(s[i])
        i += 1
    return re

def visit(link:str):
    resp1 = requests.get(link,headers={"User-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15"})
    if 200 <= resp1.status_code <300 :
        dataxml = bs(resp1.text,'lxml')
        visited = dataxml.find_all(class_ = 'NumberBoard-itemValue')
        return str_to_int(visited[1]["title"])

if __name__ == '__main__' :
    with open("settings.json",'r') as f:
        lib = json.load(f)
    con =  pymysql.connect(host='localhost',user=lib["user"],passwd=["pass"])
    cur = con.cursor()
    cur.execute("use summer")
    for _ in tqdm(range(1,5)) :
        list=connect()
        now_time = datetime.datetime.now().year*100000000+datetime.datetime.now().month*1000000+datetime.datetime.now().day*10000+datetime.datetime.now().hour*100+datetime.datetime.now().minute
        if list != None :
            for listone in tqdm(list) :
                title = listone["target"]["titleArea"]["text"]
                description = listone["target"]["excerptArea"]["text"]
                hot = str_to_int(listone["target"]["metricsArea"]["text"])
                link = listone["target"]["link"]["url"]
                visitors = visit(link)
                answers = listone["feedSpecific"]["answerCount"]
                time.sleep(0.01)
                cur.execute(f"insert into zhihu values('{title}','{description}',{hot},{visitors},{answers},{now_time})")
        con.commit()
        time.sleep(900)
    con.close()
    
