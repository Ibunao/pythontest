# -*- coding:utf-8 -*-
import os
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import requests
import pickle


def login(url, name, password):
    driver.get(url)
    # 分辨率1366 x 768
    driver.set_window_size(1366, 768)
    # driver.maximize_window()
    print(driver.title)
    # 这个是最垃圾的等待，都定死啦
    time.sleep(3)

    driver.save_screenshot("itcast.png")
    login_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "#js-header > div > div > div.Header-right > div.Header-login-wrap > div > a:nth-child(2)")))
    # driver.find_element_by_link_text("登录").click()
    # 点击登录按钮
    login_button.click()

    time.sleep(1)
    # 生成新的页面快照
    driver.save_screenshot("itcast2.png")
    # 这个时候我们用二维码登录，设置最多等待3分钟，如果登录那个区域是可见的，就登录成功
    WebDriverWait(driver, 180).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR,
                                          "#js-header > div > div > div.Header-right > div.Header-login-wrap > div > a > span.UserInfo-nickname")))

    print("登录成功")
    # 保存cookie到cookies.pkl文件
    session = requests.Session()
    # 获取cookie
    cookies = driver.get_cookies()
    # 把cookie写入文件
    if not os.path.exists("cookie"):
        os.mkdir("cookie")
    pickle.dump(cookies, open("./cookie/cookies.pkl", "wb"))


def login_with_cookie(url):
    # driver.get("https://www.douyu.com")
    driver.get(url)
    # 分辨率1366 x 768
    driver.set_window_size(1366, 768)
    # driver.maximize_window()
    time.sleep(2)
    # 把cookie文件加载出来
    with open("./cookie/cookies.pkl", "rb") as cookiefile:
        cookies = pickle.load(cookiefile)
    for cookie in cookies:
        print(cookie)
        driver.add_cookie(cookie)
    time.sleep(3)
    driver.refresh()
    # 如果cookie没有登录成功，重新用二维码登录
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,
                                              "#js-header > div > div > div.Header-right > div.Header-login-wrap > div > a > span.UserInfo-nickname")))
    except:
        print("对不起，使用cookie登录失败，请重新扫描二维码登录")
        login(url, " ", " ")

    print("登录成功")

    print(driver.title)


def send_barrage():
    while (True):
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))).send_keys(
            "好听")

        time.sleep(1)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > div"))).click()
        # 清空输入框信息
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))).clear()
        print("好听")

        time.sleep(3)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))).send_keys(
            "无敌了")
        time.sleep(1)
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > div"))).click()
        # 清空输入框信息
        wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "#js-player-asideMain > div > div.layout-Player-chat > div > div.ChatSpeak > div.ChatSend > textarea"))).clear()
        print("无敌了")

        time.sleep(3)


if __name__ == "__main__":

    # 手动登录
    options = webdriver.ChromeOptions()
    prefs = {
        "profile.default_content_setting_values.plugins": 1,
        "profile.content_settings.plugin_whitelist.adobe-flash-player": 1,
        "profile.content_settings.exceptions.plugins.*,*.per_resource.adobe-flash-player": 1,
        "PluginsAllowedForUrls": "https://www.douyu.com"
    }
    options.add_experimental_option("prefs", prefs)
    options.add_argument('--ignore-certificate-errors')

    # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    options.add_argument('--headless')

    driver = webdriver.Chrome(executable_path="./driver/mac/chromedriver", chrome_options=options)

    # 隐式等待是全局性的，只要用了driver.findxx没有第一时间找到元素，就会等待5s，当然一般都被用wait覆盖掉了
    driver.implicitly_wait(5)
    # 显示等待是定向性的，最大等待时间10s,每次检测元素有没有生成的时间间隔300ms，过了最大等待时间抛出异常
    wait = WebDriverWait(driver, timeout=10, poll_frequency=300)

    url = 'https://www.douyu.com/643037'
    name = ""
    password = ""
    if os.path.exists("./cookie/cookies.pkl"):
        print("当前目录下存在斗鱼登录的cookie文件，将为您自动登录")
        login_with_cookie(url)
    else:
        print("当前目录下不存在斗鱼登录的cookie文件")
        login(url, name, password)
    send_barrage()