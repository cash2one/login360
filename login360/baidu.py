# coding = utf-8
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
file1 = open("ip.txt",'r')

def proxyTest(proxy):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server=http://%s' % PROXY)
    driver = webdriver.Chrome(chrome_options = chrome_options)
    try:
        driver.get('http://www.baidu.com')
        driver.implicitly_wait(3)
        title = driver.title
        if "www.baidu.com" in title:
        	driver.quit()
        	raise
        print "driver title:%s"%driver.title
    except Exception,e:
        print "print driver title failed:%s"%e
        driver.quit()
        pass
    else:
        return 1
while(1):
	fl = file1.readline()
	if fl:
		s = fl.split()
		ip = s[0]
		port = s[1]
		PROXY = "%s:%s"%(ip,port)
        print PROXY 
        p = proxyTest(PROXY)
#inputElement = driver.find_element_by_xpath("//*[@id='kw1']")
#inputElement.send_keys("")
#driver.find_element_by_xpath("//*[@id='su1']").click()

