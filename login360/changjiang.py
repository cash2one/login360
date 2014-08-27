# coding = utf-8
from selenium import webdriver
import time
import string
import random
from random import choice
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
def select(name):
    list = []
    for line in open("%s"%name):
        if "----" in line:
           list.append([line.split("----")[0].strip().strip("\n"),line.split("----")[1].strip().strip("\n")]) 
        else:
           list.append(u"%s"%line.strip().strip("\n"))
        
    return choice(list)
def redIp():
    list = []
    for line in open("ip.txt",'r'):
       if len(line.strip().split())>1:
           PROXY = "%s:%s"%(line.strip().split()[0],line.strip().split()[1])
           list.append(PROXY)
       elif ":" in line:
            PROXY= "%s:%s"%(line.strip().split(":")[0],line.strip().split(":")[1])
            list.append(PROXY)
       return choice(list)
def deleteIp(delete):
    list = []
    file = open("ip.txt",'r')
    for line in file:
        if  len(line.strip().split())>1:
            PROXY= "%s:%s"%(line.strip().split()[0],line.strip().split()[1])
            list.append(PROXY)
        elif ":" in line:
            PROXY= "%s:%s"%(line.strip().split(":")[0],line.strip().split(":")[1])
            list.append(PROXY)
    file.close()
    file = open("ip.txt","w+")
    for i in list:
        if i != delete:
            file.write("%s"%i)
            file.write("\n")
    file.close()

class webDrive:
    def __init__(self):
        self.flag = 0
        self.sleepTime = 3
        #获取登陆名和密码
        self.user_passwd = select("user.txt")
        print self.user_passwd
        #用户名
        self.u_name = string.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 13)).replace(' ','')
        #任务开始时间
        self.begin=time.time()
        # 初始化driver
#        self.proxyTest()
        self.driver = webdriver.Chrome()
    def proxyTest(self):
        self.ip_Port = redIp()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=http://%s' % self.ip_Port)
        print self.ip_Port
        self.driver = webdriver.Chrome(chrome_options = chrome_options)
    def sleep(self):
        time.sleep(self.sleepTime)
    def searchKeyWords(self):
        kw = []
        for line in open("keywords.txt"):
            kw.append(u"%s"%line.strip().strip("\n"))
        return choice(kw)
    def login(self):
        try:
            self.driver.get('http://www.so.com')
            WebDriverWait(self.driver,2).until(EC.presence_of_element_located((By.ID,"user-login")))
        except Exception,e:
            print "open www.so.com fail:%s"%e
            #deleteIp('%s'%self.ip_Port)
            self.closeWebDrive()
            return "loginTimeOut"
        print self.driver.title
        while(1):
            try:
                self.driver.find_element_by_id("user-login").click()
                WebDriverWait(self.driver,30).until(EC.presence_of_element_located((By.ID,"loginAccount")))
                break
            except Exception,e:
                if time.time()-self.begin >60:
                    self.closeWebDrive()
                    return "loginTimeOut"
                print "find element user-login faile:%s"%e
        
        self.driver.find_element_by_id("loginAccount").send_keys("%s"%self.user_passwd[0])
        self.driver.find_element_by_id("lpassword").send_keys("%s"%self.user_passwd[1])
        self.driver.find_element_by_id("loginSubmit").click()
        while(1):
            try:
                WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.ID,"loginAccount")))
            except Exception,e:
                print e
                break 
            else:
                 if time.time()-self.begin > 60:
                    self.closeWebDrive()   
    def checkUserName(self):
        self.sleep()
        try:
            self.driver.find_element_by_id("pspUserName").send_keys("%s"%self.u_name)
            self.driver.find_element_by_id("btn-submitName").click()
        except Exception,e:
            print "find element pspUserName failed:%s"%e
            pass
    def search(self):
       self.sleep()
       t1=time.time()
       while(1):
            try:
                WebDriverWait(self.driver,3).until(EC.presence_of_element_located((By.ID,"btn-submitName")))
            except:
                try:
                    inputElement = self.driver.find_element_by_id("input")
                    inputElement.clear()
                    inputElement.send_keys(u"%s"%self.searchKeyWords())
                    self.sleep()
                    self.driver.find_element_by_id("search-button").click()
                    self.sleep()
                    break
                except :
                    try:
                        inputElement = self.driver.find_element_by_id("keyword")
                        inputElement.clear().send_keys(u"%s"%self.searchKeyWords())
                        self.sleep()
                        self.driver.find_element_by_id("su").click()
                        self.sleep()
                        break
                    except Exception,e:
                        print "find element search-button faile:%s"%e
                        self.sleep()
                        if time.time()-self.begin > 60:
                             break
                             return "searchTimeOut"
                        pass
            else:
                if time.time() -t1 >30:
                    self.closeWebDrive()
    def submitComment(self):
        try:
            self.sleep()
            self.driver.find_element_by_xpath("//*[@id='so-comment-inactive']/div/a").click()
        except Exception,e:
            print "can not find so-comment-inactive:%s"%e
            pass
        try:
            self.sleep()
            inputElement = self.driver.find_element_by_xpath("//*[@id='so_comment']/div[4]/div/div[4]/div/textarea")
        except Exception,e:
            print "can not find so-comment:%s"%e
            self.closeWebDrive()
            return
        try:
            for i in range(10):            
                self.comment = select("comment.txt")
                if self.comment != "":
                    print "comment:%s"%self.comment
                    inputElement.send_keys(u"%s"%self.comment)
                    self.sleep()
                    self.driver.find_element_by_xpath("//*[@id='so_comment']/div[4]/div/a[3]").click()
                    self.sleep()
                    break

        except Exception,e:
            print "submitComment:%s"%e
            self.closeWebDrive()
            return
        #self.driver.quit()
    def closeWebDrive(self):
        try:
            self.driver.quit()
        except Exception,e:
            print e
            pass
    def main(self):
        if self.login() != "loginTimeOut":
            if self.checkUserName() != "error":
                if self.search() != "searchTimeOut":
                   self.submitComment()
                   self.closeWebDrive()
        else:
            self.closeWebDrive()
    
if __name__ == "__main__":
    while(1):
        task = webDrive()
        task.main()
