#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import wxpy
import time
import sys

a = raw_input("press any key to continue")


def send_message(content):
    elem = browser.find_element_by_id("editArea")
    elem.clear()
    elem.send_keys(content)
    elem.send_keys(Keys.RETURN)


browser = webdriver.Chrome()
browser.get("http://web.wechat.com/")
b = raw_input("press any key to continue")
send_message("oj")
wxpy.embed()

if True:
    sys.exit(0)

browser.maximize_window()  # 窗口最大化
browser.find_element_by_name('wd').send_keys('Apple')  # 按name查找.传字符串
browser.find_element_by_id('su').click()  # 按id查找.单击

time.sleep(2)
actions = ActionChains(browser)  # 创建事件链
element = browser.find_element_by_id('result_logo')  # 找到元素
actions.move_to_element_with_offset(element, 210, 180)  # 相对位置移动鼠标
actions.click()  # 单击
actions.perform()  # 执行以上步骤

browser.switch_to.window(browser.window_handles[-1])  # 切换到新打开的页面
browser.find_element_by_css_selector('.ac-gn-link.ac-gn-link-mac').click()
# Compound class names 用 css selector

browser.delete_all_cookies()  # Cookie操作详见文档
browser.refresh()  # 刷新页面

"""
按照题主要求，挨个下载的话，写个循环一直到出Error结束就行了，
可能会用到 find_element_by_xpath(") ，详见文档。
"""
