#coding=utf-8
from time import sleep
import selenium
from selenium.webdriver.remote.webdriver import WebDriver as wd
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wdw
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains as AC

from bs4 import BeautifulSoup as bs
import json
from IPython import embed
d = 0
def init():
    global d
    d = selenium.webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    d.get("https://webvpn.tsinghua.edu.cn/login")
    user_name = wdw(d,10).until(EC.presence_of_element_located((By.NAME,"username")))
    password = wdw(d,10).until(EC.presence_of_element_located((By.NAME,"password")))
    with open("settings.json",'r') as f:
        lib = json.load(f)
    user_name.send_keys(lib["username"])
    password.send_keys(lib["password"])
    butt = d.find_element(By.CLASS_NAME,"el-button-login")
    butt.click()
    element = wdw(d,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"[title=信息门户]")))
    element.click()
    d.switch_to.window(d.window_handles[-1])
    element = wdw(d,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"#userName")))
    element.send_keys(lib["username"])
    element = wdw(d,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,"[name=password]")))
    element.send_keys(lib["password"])
    element = wdw(d,30).until(EC.presence_of_element_located((By.CSS_SELECTOR,".but")))
    element = element.find_element(By.CSS_SELECTOR,"[type=image]")
    element.click()
    element = wdw(d,10).until(EC.presence_of_element_located((By.LINK_TEXT,"全部成绩")))
    element.click()
    d.switch_to.window(d.window_handles[-1])#switch to grade
    d.implicitly_wait(10)
    element = d.find_element(By.TAG_NAME,"html")
    str = element.get_attribute('innerHTML')
    str = '<html>\n' + str + '\n</html>'
    xml = bs(str,'lxml')
    element = xml.find_all("body")
    element = element[0].find_all("table")
    element = element[2].find_all("div")
    return element

def calculate(list):
    first_credit = 0 
    first_sum = 0
    second_credit = 0
    second_sum = 0
    for i in range(12,len(list),9):
        if list[i+7].text[-1] == '1':
            if list[i+5].text.strip() != 'N/A' :
                first_credit += int(list[i+2].text)
                first_sum += int(list[i+2].text)*float(list[i+5].text.strip())
        else:
            if list[i+5].text.strip() != 'N/A' :
                second_credit += int(list[i+2].text)
                second_sum += int(list[i+2].text)*float(list[i+5].text.strip())
    print(F"first semester your GPA is {first_sum/first_credit}")
    print(F"second semester your GPA is {second_sum/second_credit}")
    print(f"your final GPA is {(first_sum+second_sum)/(first_credit+second_credit)}")

if __name__ == "__main__" :
    calculate(init())