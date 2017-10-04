from splinter import Browser
from pyvirtualdisplay import Display
import databaseConfig
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
import re
import hashlib
import json
from contextlib import closing
class a ():
    def run(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
            'referer': 'https://www.daydaycook.com'}
        cnx = databaseConfig.dbconn("")
        for a in range(122,123):
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
            browser.execute_script("pageSkip("+str(a)+");")
            time.sleep(1)
            # handles = set(browser.window_handles)
            # handles.remove(browser.current_window_handle)
            # browser.switch_to_window(handles.pop())
            htmlCode = browser.page_source
            browser.close()
            display.popen.terminate()

            soup = BeautifulSoup(htmlCode, "lxml")
            items = soup.find("div",{"class":"resultList justify three"})
            for item in items.findAll("div",{"class":"box"}):
                 href =  item.a.get("href")
                 token = hashlib.sha256(href).hexdigest()
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
                 ingredientJson = json.dumps(tag, encoding='UTF-8', ensure_ascii=False)
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
                 ##Step end
                 ##Time
                 cookingTime = soup.find("div",{"class":"timeLen"}).find_all("span")[1].text

                 try:
                     with closing(cnx.cursor()) as cursor:
                         cursor.execute(
                             "INSERT INTO recipes(`token`,`title`,`ingredients`,`cooking_time`,`display_content`,`source`,`article_url`,`created_time`,`updated_time`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)ON DUPLICATE KEY UPDATE `title` = %s, `updated_time` = %s",
                             (
                                 token, title,ingredientJson,cookingTime, stepJson, 'dayCook',href, int(time.time()),
                                 int(time.time()),
                                 title,  int(time.time()),
                             )
                         )
                     cnx.commit()
                 except TypeError as e:
                     print(e)
                     print "error"
                 try:
                     with closing(cnx.cursor()) as cursor:
                         cursor.execute(
                             "INSERT INTO recipes_details(`token`,`content`,`created_time`,`updated_time`) VALUES (%s,%s,%s,%s)ON DUPLICATE KEY UPDATE `updated_time` = %s",
                             (
                                 token, r.content,int(time.time()),int(time.time()),
                                 int(time.time()),
                             )
                         )
                     cnx.commit()
                 except TypeError as e:
                     print(e)
                     print "error"
                 time.sleep(2)

        cnx.close()




k = a()
k.run()