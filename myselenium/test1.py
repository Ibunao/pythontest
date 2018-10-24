from selenium import webdriver
import time

driver = webdriver.Chrome(executable_path="./driver/chromedriver.exe")
driver.get('https://www.douyu.com/1983057')

time.sleep(180)
print('睡眠结束')
driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/textarea').send_keys('不孬')
driver.find_element_by_xpath('//*[@id="js-player-asideMain"]/div/div[2]/div/div[2]/div[2]/div').click()
print('查看信息吧')
time.sleep(600)
driver.quit()