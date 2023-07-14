import undetected_chromedriver as uc
options = uc.ChromeOptions()
from pyvirtualdisplay import Display
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC
import time 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"])     # << this

display = Display(visible=0, size=(1920, 1080))
display.start()
options = uc.ChromeOptions()
options.add_argument("--user-data-dir=/home/pi/chrome/user")
options.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox"]) 
options.add_argument("--profile-directory=Default")

options.binary_location = "/usr/bin/chromium"
#browser = uc.Chrome(options=options)
browser = uc.Chrome(options=options,driver_executable_path="/usr/local/bin/chromedriver")
print("open")
browser.save_screenshot("/home/pi/chrome/screenshot/1.png")

url    = 'https://accounts.google.com/ServiceLogin'
email ="downlod3rmusik@gmail.com"
password = "123456789L0LxD"
browser.get(url)
time.sleep(5)
browser.save_screenshot("/home/pi/chrome/screenshot/2.png")

if len(email) < 1 or len(password) <1:

    print("no login data found")


# open_chrome(url,"/music/TEMP",3)
if browser.current_url[:27]  == url[:27]:
    browser.save_screenshot("/home/pi/chrome/screenshot/3.png")
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.NAME, 'identifier'))).send_keys(f'{email}\n')
    time.sleep(15)
    print("screenshot done")
    browser.save_screenshot("/home/pi/chrome/screenshot/4.png")    
    WebDriverWait(browser, 20).until(EC.visibility_of_element_located((By.NAME, 'Passwd'))).send_keys(f'{password}\n')
    browser.save_screenshot("/home/pi/chrome/screenshot/5.png")    
    
    print("successfully logged in google  ")

else:
    print("already logged in google ")