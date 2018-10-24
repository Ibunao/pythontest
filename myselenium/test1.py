from selenium import webdriver
import time
# win
# driver = webdriver.Chrome(executable_path="./driver/chromedriver.exe")
# mac
driver = webdriver.Chrome(executable_path="./driver/mac/chromedriver")
driver.get('https://www.douyu.com/5227917')

time.sleep(120)
print('睡眠结束')
driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea').send_keys('节日快乐！此信息由程序发出')
driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div').click()
print('查看信息吧')
time.sleep(60)
driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea').send_keys('哈哈哈哈哈哈！')
driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div').click()

time.sleep(600)
driver.quit()