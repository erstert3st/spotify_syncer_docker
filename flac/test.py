import os
import random
import re
import time
import command
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from captcha import captcha
from custom_except import captchaSolvedExcept
from os import environ
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from xvfbwrapper import Xvfb

class SeleniumScraper(object):
    def __init__(self,downloadDir ,ua="",  anwesend=False,hoster=[],db=""):
        environ['LANGUAGE'] = 'en_US'
        self.url = ""
        self.captchaSolvedChecker = False
        self.ua = ua if len(ua) > 0 else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11"
        self.xy=[1920,1080]
        
    def __del__(self):
      #  self.disp.stop()
        self.browser.quit()
        print("done")
    
    def open_Chrome(self,link,downloadDir,timer=3):
        self.user_data_dir=os.getenv("CHROME_USR_DIR","/home/user/.config/google-chrome/")
        try: command.run(['pkill', 'chrome']) 
        except:print("no chrome open")
        self.getChromeData(self.user_data_dir,True,downloadDir=downloadDir)
        fixBrowser = uc.Chrome(user_data_dir=self.user_data_dir,options=self.options)
        time.sleep(2)
        fixBrowser.close()
        time.sleep(1)
        #if True: self.activateRemoteDebugging()
        try: command.run(['pkill', 'chrome']) 
        except:print("no chrome open")
       # self.browser = uc.Chrome(user_data_dir=self.user_data_dir,options=self.options)
        self.getChromeData(self.user_data_dir,True,downloadDir=downloadDir)
        self.browser = uc.Chrome(headless=True, user_data_dir=self.user_data_dir,options=self.options)
        self.url = link
        time.sleep(2)
        self.getWaitUrl(self.url,timer)  # add lang
        return True 
    
    def checkBrowser(self):
        url = "https://cine.to/"
       # url = "chrome://version"
        self.open_Chrome(url,"/removeMe/",7)
        self.browser.save_screenshot(time.strftime("%Y-%m-%d_%H-%M.%S", time.localtime()) + ".png")
        time.sleep(50)
        return True
    

    def activateRemoteDebugging(self):
    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
        #debugpy.listen(5678)
        print("Waiting for debugger attach")
        #debugpy.wait_for_client()
      #  debugpy.breakpoint()

    def getChromeData(self,userDir="",skipRemoveError=False,downloadDir=""):
        self.url, self.Browser, self.title = "","",""
        options=""
        if os.getenv("CHROME_USR_DIR") is not None:
             vdisplay = Xvfb(width= self.xy[0], height= self.xy[1], colordepth=16)
           #  vdisplay = Xvfb(width=1500, height=730, colordepth=16)
             vdisplay.start()
            #self.disp = Display(backend="xvnc",size=(100, 60),color_depth=24 ,rfbport=2020)
           # self.disp.start()
        options = uc.ChromeOptions()
        options.add_argument('--disable-gpu')
        options.add_argument("--no-sandbox")
        #self.options.add_argument("-user-agent='"+self.ua+"'")
        #options.add_argument('--remote-debugging-port=9000')
       # options.headless = True
       # options.add_argument("--headless=new")
        #options.add_argument("detach", True)
        #options.add_argument("--load-extension=/"+os.getenv("UBLOCK_DIR","home/user/Schreibtisch/SCRPPER/seleniumTest/uBlock0.chromium"))
        options.add_argument("--enable-logging= --v=1 > log.txt 2>&1")
       # options.add_argument("--enable-logging=stderr --v=1")
        options.add_argument("--profile-directory=Defau1t")
        #options.debugger_address = "localhost:9222"
        #options.add_argument("--lang=en")
        #options.add_experimental_option('prefs', {'intl.accept_languages':  "de,DE"})
        #options.add_argument("--window-size="+str(self.xy[0])+","+str(self.xy[1]))
        options.add_argument("--disable-session-crashed-bubble") #downloadDir,
      #  temp = {"download.default_directory": '/home/user/Musik/dir/TEMP'}
       # options.add_experimental_option("prefs",temp )
        self.options = options
        return options
        #options.add_argument("--profile-directory=Default")
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)

    def getWaitUrl(self,url,timer=3): # add ad waiter
        self.browser.get(url)
        time.sleep(timer)
    
if __name__ == "__main__":
    print("start")
    fetcher = SeleniumScraper("/home/user/Musik/dir/TEMP","db")
    fetcher.checkBrowser()