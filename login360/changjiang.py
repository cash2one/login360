# coding = utf-8

from selenium import webdriver
import time
import string
import random
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
site = ['www.bybyabc.com ','www.cjhospital.com','www.cjhospital.com ','http://www.cjhospital.com/lianxiwomen/ ','www.zgxby.com','http://www.cjhospital.com/nvxingbuyun/',\
'http://www.cjhospital.com/nvxingbuyunjianchazhenduan/9519/2348.shtml','www.cjhospital.com...xiwomen/&nbsp']
sou = ['上海长江医院 ','上海长江医院怎么样 ','上海长江医院地址 ','上海长江医院好不好','上海长江医院好吗 ','上海长江医院好 ','不孕不育医院哪家好 ',\
'上海不孕不育医院哪家好 ','上海不孕不育医院哪个好','不孕不育检查项目 ','不孕不育检查项目有哪些','女性不孕不育检查项目']
def webDrive(name,passwd):
    t=time.time()
    flag = 0
    u_name = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 13)).replace(' ','')
    driver = webdriver.Chrome()
    driver.get('http://www.so.com')
    time.sleep(1)
    while(1):
        try:
            driver.find_element_by_id("user-login").click()
            time.sleep(2)
            break
        except Exception,e:
            print "find element user-login faile:%s"%e
    while(1):
        try:
            inputElement = driver.find_element_by_id("loginAccount")
            break
        except Exception,e:
            print "find element loginAccount failed:%s"%e
            time.sleep(2)
            pass
    inputElement.send_keys("%s"%name)
    time.sleep(1)
    inputElement = driver.find_element_by_id("lpassword")
    inputElement.send_keys("%s"%passwd)
    time.sleep(1)
    for i in range(2):
        try:
            userName = driver.find_element_by_id("pspUserName")
            userName.send_keys("%s"%u_name)
            driver.find_element_by_id("btn-submitName").click()
            time.sleep(30)
            break
        except Exception,e:
            print "find element pspUserName failed:%s"%e
            time.sleep(1)
            flag = i
            pass
    if flag < 10:
        for i in sou:
            while(1):
                try:
                   if i == sou[0]:
                       inputElement = driver.find_element_by_id("input")
                       inputElement.send_keys(u"%s"%i)
                       time.sleep(2)
                       driver.find_element_by_id("search-button").click()
                       time.sleep(3)
                       break
                   else:
                       inputElement = driver.find_element_by_id("keyword")
                       time.sleep(1)
                       inputElement.clear()
                       time.sleep(1)
                       inputElement.send_keys(u"%s"%i)
                       time.sleep(2)
                       driver.find_element_by_id("su").click()
                       time.sleep(3)
                       break
                except Exception,e:
                   print "find element search-button faile:%s"%e
                   time.sleep(3)
                   if time.time()-t > 300:
                       driver.quit()
                       return
                   pass
            #li = driver.find_element_by_link_text("上海长江医院")
            ul = len(driver.find_elements_by_css_selector("ul#m-result>li"))
            print "ul:%s"%ul
            for i in range(1,ul):
               time.sleep(3)
               try:
                   #li = driver.find_element_by_xpath("//*[@id='m-result']/li[%d]/h3/a"%i).text
                   li = driver.find_element_by_xpath("//*[@id='m-result']/li[%d]/p[2]/cite"%i).text
                   print "li:%s"%li
                   for s in site:
                       if s in li:
                          driver.find_element_by_xpath("//ul[@id='m-result']/li[%d]/p/div"%i).click()
                          print "搜索排名：%s %d"%(s,i)
                          time.sleep(2)
                         
                          
               except Exception ,e:
                   print "find element id=m-result/li[%d] faile:%s"%(i,e)
                   pass     
            print driver.title
        driver.quit()
    else:
        driver.quit()
    
if __name__ == "__main__":
    file = open("email.txt",'r')
    while(1):
       f = file.readline()
       if f:
          s = f.split("----")
          user = s[0]
          password = s[1]
          print user,password
          if user and password:
             webDrive(user,password)
             time.sleep(3)
