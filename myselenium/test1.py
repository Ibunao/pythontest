from selenium import webdriver
import time
from pymongo import MongoClient
import re

# win
driver = webdriver.Chrome(executable_path="./driver/chromedriver.exe")
# mac
# driver = webdriver.Chrome(executable_path="./driver/mac/chromedriver")
driver.get('https://www.douyu.com/5227917')

def cut_text(text, lenth):
    textArr = re.findall('.{' + str(lenth) + '}', text)
    textArr.append(text[(len(textArr) * lenth):])
    return textArr

time.sleep(120)
print('睡眠结束')
# 连接mongo
client = MongoClient('118.25.38.240', 27017)
# 选择使用的数据库
db_auth = client['spider_test']
# 验证登陆
db_auth.authenticate("spider", "spider123")
db = client['spider_test']
temp = db['xiushibaike'].find({})
for item in temp:
    print(item['content'])
    if len(item['content']) > 25 :
        arr = cut_text(item['content'], 50)
        for cont in arr :
            driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea').send_keys(cont)
            driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div').click()
            print('查看信息吧')
            time.sleep(5)
        time.sleep(30)


time.sleep(300)
driver.quit()


