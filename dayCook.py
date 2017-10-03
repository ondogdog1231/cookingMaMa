from splinter import Browser
from pyvirtualdisplay import Display
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class a ():
    def run(self):
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
        time.sleep(5)
        # handles = set(browser.window_handles)
        # handles.remove(browser.current_window_handle)
        # browser.switch_to_window(handles.pop())
        htmlCode = browser.page_source
        browser.close()

        soup = BeautifulSoup(htmlCode, "xml")
        items = soup.find("div",{"class":"resultList justify three"})
        for item in items.findAll("div",{"class":"box"}):
            print item.a



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