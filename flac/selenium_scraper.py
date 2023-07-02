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
from xvfbwrapper import Xvfb
#from chromedriver_py import binary_path # this will get you the path variable

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
            options.binary_location = "/usr/bin/chromium"
            #options.binary_location = "/usr/bin/brave-browser"
            options.add_argument("--user-data-dir="+ os.getenv("CHROME_USR_DIR"))
            options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"]) 
            vdisplay = Xvfb(width= self.xy[0], height= self.xy[1], colordepth=16)
           #  vdisplay = Xvfb(width=1500, height=730, colordepth=16)
            vdisplay.start()
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
        options.add_argument("--load-extension="+os.getenv("UBLOCK_DIR","/home/user/Schreibtisch/SCRPPER/seleniumTest/uBlock0.chromium"))
        #options.add_argument("--enable-logging= --v=1 > log.txt 2>&1")
        #options.add_argument("--enable-logging=stderr --v=1")
        options.add_argument("--profile-directory=Default")
        options.add_argument("--disable-dev-shm-usage")
        
        #options.add_argument("--profile-directory=Defau1t")
       # options.debugger_address = "127.0.0.1:9223"
        #options.add_argument("--lang=en")
        #options.add_experimental_option('prefs', {'intl.accept_languages':  "de,DE"})
        options.add_argument("--window-size="+str(self.xy[0])+","+str(self.xy[1]))
       # options.add_argument("--disable-session-crashed-bubble") #downloadDir,
        #temp = {"download.default_directory": '/home/user/Music/dir/TEMP'}
       # options.add_experimental_option("prefs",temp )

        options.add_experimental_option("prefs", {"download.default_directory": downloadDir,
                                            "download.prompt_for_download": False,
                                            "download.directory_upgrade": True,
                                            "profile.default_content_setting_values.notifications":2,
                                            "safebrowsing.enabled": True})
        self.options = options
        return options
        #options.add_argument("--profile-directory=Default")
        #vdisplay = Xvfb(width=1920, height=1080, visible=0)

    def close_browser(self):
        if hasattr(self, 'browser') is True:
            self.browser.quit()
        print("close")
    
    def click_wait(self,selectorType=By.CSS_SELECTOR,selector="",timer=5,element=""):
        if type(element) == str:
            element= self.browser.find_element(selectorType,selector)
        element.click()
        time.sleep(timer)
    
    def get_wait_url(self,url,timer=4): # add ad waiter
        self.browser.get(url)
        time.sleep(timer)
    
    def find_solve_captcha(self, iframe, dry_run=False):
        print("start find_solve_captcha")
        from .captcha import captcha
        from  .custom_except import captcha_solved_except

        time.sleep(random.randint(5, 15))
        # return "restart"
        error_info = False
        self.browser.switch_to.frame(iframe)
        #self.browser.save_screenshot("pics/" + str(y) + ".png")
        print("switching to the recaptcha iframe")
        # clicking to request the audio challange
        mayCaptcha = self.browser.find_elements(By.XPATH, '//*[@id="recaptcha-audio-button"]')
        if len(mayCaptcha) < 1 : 
        #LOGGGER !!!!! 
            return False
        elif dry_run is True:
            return True
        try:
            mayCaptcha[0].click()
        except:
            #captcha is not clickable so it might be solved ?
            print("captcha is not clickable so it might be solved ?")
            return True

        while error_info is False:
            print("find_solve_captcha -> captcha found!!!")
            time.sleep(3)
            audio_url = self.browser.find_elements(By.CLASS_NAME, "rc-audiochallenge-tdownload-link")[0].get_attribute('href')
            time.sleep(1) 
            if len(audio_url) < 1: raise Exception
            # verifying the answer
            solution = captcha().captcha_solver(audio_url)
            print("captchaSolver -> captcha solved")
            if self.captcha_solved is False:
                self.captcha_solved = True
            else: raise captcha_solved_except
            time.sleep(random.randint(5, 9))
            # answer_input
            self.browser.find_element(By.ID, 'audio-response').send_keys(solution)
            time.sleep(random.randint(1, 3))
            # submit_button
            self.browser.find_element(By.XPATH, '//*[@id="recaptcha-verify-button"]').click()
            time.sleep(10)        
            error_element = ""
            error_element = self.browser.find_elements(By.CSS_SELECTOR,"#rc-audio > div.rc-audiochallenge-error-message")
            print("find_solve_captcha -> captcha solved!!!")
            if len(error_element) > 0 and error_element[0].text == "Multiple correct solutions required - please solve more.":
                print("find_solve_captcha -> second captcha needed solved!!!")
                error_info = True
                self.browser.switch_to.default_content()
                self.find_solve_captcha(iframe)
            return True
        time.sleep(7)

    def beep(self):
        duration = 1 # seconds
        freq = 100  # Hz
        os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))        

    def captcha_check(self,selectorType,selector, dry_run=False):
        for x in range(1, 2):     
            captcha_search =  self.browser.find_elements(selectorType,selector)
            if len(captcha_search) > 0:             
                captchaReturn = self.find_solve_captcha(captcha_search[0],dry_run)
                self.browser.switch_to.default_content()
                return captchaReturn
                break
            #   catch b  captchaLock! 
        self.browser.switch_to.default_content()
        return False

    def search_click(self,search,selector, querry,button=""):
        # find the search box element and enter a search term
        search_box = self.browser.find_element(selector, search)
        search_box.send_keys(querry)
        # find the search button and click it
        if(len(button) > 1):
            self.browser.find_element(selector, button).click()
        time.sleep(5)
        #self.url = self.browser.current_url


    def download_flac(self,file_path,download_path):  
        modul  = "musicDownloader"
        file_name =  file_path[:-4]
        self.open_chrome("https://free-mp3-download.net/" ,downloadDir=download_path,timer=15)  
       # self.get_wait_url("https://free-mp3-download.net/")
        # playlistPattern = r"^\d{2,3}\s-"

        #if re.search(playlistPattern, file_name):
            #  file_name = re.sub(playlistPattern, "", file_name, count=1)
        print("chrome opend link")
        #self.browser.save_screenshot("/app/flac/page1.png")  

        self.search_click(search= "q", selector=By.ID, querry=file_name,button="snd")
        #loop and check may add loop first child 
        print("search_click done")

        self.click_wait(By.CSS_SELECTOR,"#results_t > tr:nth-child(1) > td:nth-child(3) > a > button",10) 
        self.browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")      
        quali = self.browser.find_elements(By.CSS_SELECTOR, "#quality-row > div:nth-child(3) > p > label")
        print("cehck element")
        print(len(quali))
        if len(quali) < 0:
            #LOGGGERT AND HANDLING #TODO: 
            quali =  self.browser.find_element(By.CSS_SELECTOR, "#quality-row > div:nth-child(2) > p > label")
        else:
            quali = quali[0]
        self.click_wait(element=quali,timer=3)
        print("download_flac -> song found, start looking for captcha")
        captcha =  self.browser.find_elements(By.ID,"captcha") 
        if len(captcha) > 0: 
            self.click_wait(element=captcha[0],timer=5)
            #Handle second Captcha!
            captcha_found = self.captcha_check(By.CSS_SELECTOR,"body > div:nth-child(13) > div:nth-child(4) > iframe",dry_run=True)
            print("captcha dry run")
            if captcha_found is True: # Todo captcha handler more flexi
                print("captcha dry run -> found")
                self.captcha_solved_checker = self.captcha_check(By.CSS_SELECTOR,"body > div:nth-child(13) > div:nth-child(4) > iframe")
            print("captcha done -> default content")

        print("start download")
        self.click_wait(selectorType=By.TAG_NAME,selector="button",timer=3)
        time.sleep(25)
        print("download should be finished") # Todo check if file is done
        return True
if __name__ == "__main__":
     print("start")
     fetcher = selenium_scraper("/home/user/Musik/music/TEMP","db")
     #fetcher.login_google("https://accounts.spotify.com/authorize?client_id=33bbbfe2ba9a486ebd39ff4db06c689d&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A9090&code_challenge_method=S256&code_challenge=injfBYkw9jRd8CBtKrWoagEC-Vr2mz-TVgHJKCBrpQ8&scope=+playlist-read-collaborative++playlist-read-private+user-library-read")
     HI =fetcher.login_google()
     print(HI)