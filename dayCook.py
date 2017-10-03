from splinter import Browser
from pyvirtualdisplay import Display
import databaseConfig
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re
import json
class a ():
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'referer': 'https://www.hksilicon.com'}
        display = Display(visible=0, size=(800, 600))
        display.start()

        browser = webdriver.Firefox()
        # browser.get('https://www.towngascooking.com/tc/Recipe/')
        browser.get('http://www.daydaycook.com/daydaycook/hk/website/recipe/list.do')
        #It can go to other page but wrong page
        # element = browser.find_element_by_id("currentPage")
        # element.send_keys(3)
        # browser.find_element_by_id("pageListForm").submit()
        # browser.find_element_by_class_name("dinggou").click()
        ##
        # browser.execute_script('return $(\"(.pagination a\").eq(3).click();')
        time.sleep(5)
        # browser.execute_script("getList(4);")
        a = 2
        browser.execute_script("pageSkip("+str(a)+");")
        time.sleep(1)
        # handles = set(browser.window_handles)
        # handles.remove(browser.current_window_handle)
        # browser.switch_to_window(handles.pop())
        htmlCode = browser.page_source
        browser.close()

        soup = BeautifulSoup(htmlCode, "lxml")
        items = soup.find("div",{"class":"resultList justify three"})
        for item in items.findAll("div",{"class":"box"}):
             href =  item.a.get("href")
             r = requests.get(href, headers=headers)
             soup = BeautifulSoup(r.content, "lxml")
             title =  soup.find("div",{"class":"title"}).b.text
             print title
             # ingredients Start
             ingredients =soup.find("div",{"class":"table"}).table.find_all("tr")
             tag = {}
             for tr in ingredients:
                _ingredients =  tr.find_all('td')[0].text
                _grading =  re.sub('[\s+]', '', tr.find_all('td')[1].text)
                tag[_ingredients] = _grading
             tagJson = json.dumps(tag, encoding='UTF-8', ensure_ascii=False)
             # ingredients End

             ##Step start
             stepList = soup.find("div",{"class":"stepList"}).find_all("div",{"class":"list justify"})
             stepNo = 0
             stepArr = []
             stepImgArr = []
             for _step in stepList:
                 stepImgArr.append(_step.img.get("data-src"))
                 stepArr.append(_step.pre.text)
             stepZip = zip(stepArr, stepImgArr)
             stepJson = json.dumps(stepZip, encoding='UTF-8', ensure_ascii=False)
             print stepJson
             ##Step end

             time.sleep(2)
             exit()



        # driver.findElement(By.linkText("Add a New Credit Card")).click();
        #pagination
        # print browser.find_elements_by_class_name("pagination a")
        # for item in browser.find_elements_by_class_name("pagination a"):
        #     print item
        # browser.find_elements_by_class_name("pagination a")[50].click()

        # print browser.page_source
        # print browser.execute_script("return 5+5")
        # print browser.page_source




k = a()
k.run()