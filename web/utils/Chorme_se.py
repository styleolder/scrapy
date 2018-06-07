# -*- coding: utf-8 -*-  
__author__ = 'style'
from selenium import webdriver
from scrapy.selector import Selector
import time
# 设置chromedriver不加载图片
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_opt.add_experimental_option("prefs", prefs)

#初始化浏览器添加选项
driver = webdriver.Chrome(chrome_options=chrome_opt)
driver.maximize_window()
time.sleep(5)
driver.get("https://www.baidu.com")
#通过scrapy的xpath去查找属性比selenium自带的快
t_selector = Selector(text=driver.page_source)
print t_selector.xpath('//input[@id="su"]/@value').extract_first()
#输入操作与点击操作
driver.find_element_by_xpath('//input[@id="kw"]').send_keys("style")
driver.find_element_by_xpath('//input[@id="su"]').click()
time.sleep(5)
#执行js脚本滑动 滚动条
driver.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#关闭浏览器窗口
#driver.quit()