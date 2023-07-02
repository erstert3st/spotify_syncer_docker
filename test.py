import os
import random
import json 
import command
import undetected_chromedriver as uc
from selenium.webdriver.common.keys import Keys
from os import environ
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
#from xvfbwrapper import Xvfb
#from chromedriver_py import binary_path # this will get you the path variable
from pyvirtualdisplay import Display

import debugpy

import time 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC

class selenium_scraper(object):
    def __init__(self,downloadDir="" ,ua="",  anwesend=False,hoster=[],db=""):
        environ['LANGUAGE'] = 'en_US'
        self.url = ""
        self.captcha_solved = False
        self.ua = ua if len(ua) > 0 else "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11"
        self.xy=[1920,1080]
        
    # def __del__(self):
    #   #  self.disp.stop()
    #     self.close_browser()
    #     print("done")
    
    def kill_chrome(self):
        #try: command.run(['pkill', 'brave']) 
        try: command.run(['pkill', 'chromium']) 
        except:print("no chromium open")

    def open_chrome(self,link,downloadDir,timer=3):
        self.user_data_dir=os.getenv("CHROME_USR_DIR","/home/user/Schreibtisch/spotDocker/spotify_sync_docker/dir")
        print(self.user_data_dir)
       # fixChrashes = self.get_chrome_data(self.user_data_dir,True,downloadDir=downloadDir)
        time.sleep(1)
        #if True: self.activateRemoteDebugging()
        self.kill_chrome()
       # fixChrashes = uc.Chrome(user_data_dir=self.user_data_dir,options=self.options)
        time.sleep(2)
        #fixChrashes.close() # fresh chrome for Headless needed
       # del fixChrashes
      #  self.get_chrome_data(self.user_data_dir,True,downloadDir=downloadDir)
        self.get_chrome_data(self.user_data_dir,True,downloadDir=downloadDir)
        time.sleep(1)
        self.kill_chrome()
       # self.browser = uc.Chrome(options=self.options)
        #äself.browser = uc.Chrome(options=self.options)
        #self.browser = uc.Chrome(headless=False,user_data_dir=self.user_data_dir,options=self.options)
        self.browser = uc.Chrome(options=self.options,driver_executable_path=os.getenv("CHROMEDRIVER_PATH","/home/user/Schreibtisch/spotDocker/spotify_sync_docker/test/chromedriver_x64"))
        print("chrome startet")
        #time.sleep(100)
        time.sleep(2)
        print("test")
        #self.remote_debugging()
        self.url = link
        
        print(self.url)
        self.get_wait_url(self.url,timer)  # add lang
        return True 
    #/usr/bin/google-chrome-stable'
    def check_browser(self):
       # self.remote_debugging()
       #chromium --remote-debugging-address=0.0.0.0 --remote-debugging-port=9222 --headless --disable-gpu --no-sandbox --disable-dev-shm-usage --enable-automation --window-size=1440,900 about:blank
        url = "chrome://version"
       # url = "https://nowsecure.nl/"chrome://version/
       # url = "chrome://version"
        self.open_chrome(url,"/music/TEMP",3)

        #self.browser.save_screenshot("/app/flac/version.png")  
        self.get_wait_url("https://nowsecure.nl/",3)
        #self.browser.save_screenshot("/app/flac/secure.png")    
        print(self.browser.current_url)   
        time.sleep(5)
        return True
    
    def login_google(self,login_spotify_url=""):
        url    = 'https://accounts.google.com/ServiceLogin'
        email = os.getenv("EMAIL","")
        password = os.getenv("PASSWORD","")
        self.open_chrome(url,"/music/TEMP",3)

        if len(email) < 1 or len(password):
            try:
              #  with open('/app/flac/login.txt') as f:
                with open('flac/login.txt') as f:
                    login_data = json.loads(f.read())
                    email = login_data["email"]
                    password = login_data["password"]
            except:
               print("no file found")
        
        if len(email) < 1 or len(password) <1 : 
            print("check login Vars ")
            raise Exception
        
       # self.open_chrome(url,"/music/TEMP",3)
        if self.browser.current_url[:27]  == url[:27]:
           # self.browser.save_screenshot("/app/flac/flags1.png")       
            WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
            time.sleep(2)
            WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{password}\n')
            print("successfully logged in google  ")

        else:
            print("already logged in google ")
        #self.browser.save_screenshot("/app/flac/flags12.png")       

        if len(login_spotify_url) > 1:
            if(login_spotify_url[:5] == "URL: "): login_spotify_url = login_spotify_url[5:]
            self.get_wait_url(login_spotify_url,5)
            try:
                self.click_wait(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/ul/li[1]/button/span[2]',timer=3)
            except:
                print("spotify already logged in ")
            self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")  
            self.click_wait(selectorType=By.XPATH, selector='//*[@id="root"]/div/div[2]/div/div/div[3]/button/div[1]',timer=5)
        #debugpy.breakpoint()
        time.sleep(5)
        #crash in dockerArm
        dummyVarChromiumBug = self.browser.current_url

        #dummyVarChromiumBug = "https://myaccount.google.com/chromiumBug"
        print(dummyVarChromiumBug)
        return dummyVarChromiumBug

        
    def remote_debugging(self):
    # 5678 is the default attach port in the VS Code debug configurations. Unless a host and port are specified, host defaults to 127.0.0.1
        #debugpy.listen(5678)
        self.get_wait_url("chrome://version",5)  # add lang
        self.browser.save_screenshot("/app/flac/flags.png")       
        debugpy.listen(("0.0.0.0", 5678))
        print("Waiting for debugger attach")
        debugpy.wait_for_client()
        debugpy.breakpoint()




    def get_chrome_data(self,userDir="",skipRemoveError=False,downloadDir=""):
        self.url, self.Browser, self.title = "","",""
        
        options = uc.ChromeOptions()

        print(downloadDir)
        #if in docker

        if os.getenv("CHROME_USR_DIR") is not None:
           # chrome_exe_path = "/usr/bin/google-chrome"
            #options.binary_location = chrome_exe_path
            options.binary_location = "/usr/bin/chromium-browser"
            #options.binary_location = "/usr/bin/brave-browser"
            options.add_argument("--user-data-dir="+ os.getenv("CHROME_USR_DIR"))
            options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"]) 
            display = Display(visible=0, size=(1920, 1080))
            display.start()
            
            
            #vdisplay = Xvfb(width= self.xy[0], height= self.xy[1], colordepth=16)
           #  vdisplay = Xvfb(width=1500, height=730, colordepth=16)
            #vdisplay.start()
            #self.disp = Display(backend="xvnc",size=(100, 60),color_depth=24 ,rfbport=2020)
           # self.disp.start()
       # else: options.binary_location = "/usr/bin/chromium-browser"
       # print(options.binary_location)
       # options.add_argument('--disable-gpu')
        #options.add_argument("--no-sandbox")
        #self.options.add_argument("-user-agent='"+self.ua+"'")
       # options.add_argument('--remote-debugging-address=127.0.0.1')
       # options.add_argument('--remote-debugging-port=9222')
       # options.add_argument("--headless=new")
       # options.add_argument("detach", True)
        #print("--load-extension="+os.getenv("UBLOCK_DIR","/home/user/Schreibtisch/SCRPPER/seleniumTest/uBlock0.chromium"))
        #options.add_argument("--load-extension="+os.getenv("UBLOCK_DIR","/home/user/Schreibtisch/SCRPPER/seleniumTest/uBlock0.chromium"))
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option("prefs", {"download.default_directory": downloadDir,
                                            "download.prompt_for_download": False,
                                            "download.directory_upgrade": True,
                                            "profile.default_content_setting_values.notifications":2,
                                            "safebrowsing.enabled": True})
        self.options = options
        return options


    
    def click_wait(self,selectorType=By.CSS_SELECTOR,selector="",timer=5,element=""):
        if type(element) == str:
            element= self.browser.find_element(selectorType,selector)
        element.click()
        time.sleep(timer)
    
    def get_wait_url(self,url,timer=4): # add ad waiter
        self.browser.get(url)
        time.sleep(timer)
    

if __name__ == "__main__":
     print("start")
     fetcher = selenium_scraper("/home/user/Musik/music/TEMP","db")
     #fetcher.login_google("https://accounts.spotify.com/authorize?client_id=33bbbfe2ba9a486ebd39ff4db06c689d&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A9090&code_challenge_method=S256&code_challenge=injfBYkw9jRd8CBtKrWoagEC-Vr2mz-TVgHJKCBrpQ8&scope=+playlist-read-collaborative++playlist-read-private+user-library-read")
     HI =fetcher.check_browser()
     print(HI)