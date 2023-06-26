import pytest
import os 
from flac.flacer import Flacer
from flac.selenium_scraper import selenium_scraper 
#from spotify_sync.cli import SpotifySyncApp
import shutil
from spotify_sync.cli import SpotifySyncApp

#app = SpotifySyncApp()
#app.sync_spotify()


# def test_login():
#     print("start test:")
def test_env_vars():
    #Todo: add if folder exist 
    assert  len(os.getenv("DISPLAY","")) >= 1
    assert  len(os.getenv("BASE_PATH","")) >= 1
    assert  len(os.getenv("UBLOCK_DIR","")) >= 1
    assert  len(os.getenv("SELENIUM_CLASS_PATH","")) >= 1
    assert  len(os.getenv("CHROME_USR_DIR","")) >= 1
  #  assert  len(os.getenv("EMAIL","")) >= 1
   # assert  len(os.getenv("PASSWORD","")) >= 1
    assert  len(os.getenv("CONFIG_PROFILE","")) >= 1
    assert  len(os.getenv("MANUAL_CONFIG_FILE","")) >= 1

def test_login_spotify():
    app = SpotifySyncApp()
    os.environ['CONFIG_PROFILE'] = 'myFirstProfile'
   # os.environ['MANUAL_CONFIG_FILE'] = '/home/user/Schreibtisch/spotDocker/spotify_sync_docker/config.json'
    # Call the sync_spotify() function
    app.authorize_spotify()
    assert True == True
def test_copy():
    base_path = os.getenv("BASE_PATH","/home/user/Musik/dir")
    temp_folder = os.path.join(base_path ,"TEMP")
    flacer = Flacer

    flacer.remove_folder_contents("",temp_folder)

    temp_folder_source = os.path.join(temp_folder ,"SOURCE")
    temp_folder_dest = os.path.join(temp_folder ,"DEST")
    os.mkdir(temp_folder_source)
    os.mkdir(temp_folder_dest)
    file = "myfile.txt"
    file_path = os.path.join(temp_folder , file)
    open(file_path, "x").close()
    shutil.copy2(file_path,temp_folder_dest+"/" + file)
    file_list = [entry.name for entry in os.scandir(temp_folder_dest) if entry.is_file()]
    flacer.remove_folder_contents("",temp_folder)
    assert "myfile.txt" in file_list

def test_flac_working(): #
    flacer = Flacer()
    assert  flacer.check_flac("flac_test_files/working.flac") == True

def test_flac_not_working(): #
    flacer = Flacer()
    assert  flacer.check_flac("flac_test_files/not_working.flac") == False

def test_google_login():
    print("start test:")
    selenium = selenium_scraper()
    googleLink = selenium.login_google()
    print(googleLink)
    assert googleLink.startswith("https://myaccount.google.com") 

def test_check_browser():
    print("start test:")
    selenium = selenium_scraper()
    redirect_url = selenium.check_browser()
    assert redirect_url == True

#def test_spotify_sync_authorize(): #
   # flacer = Flacer()
  #  flacer.check_flac()



#https://myaccount.google.com/?utm_source=sign_in_no_continue
# def test_spotify_sync_dry_run(): #
#     print("start test:")

def test_download_flac():
    flacer = Flacer() #Todo add BasePath after test than list files and than remove file 
    hi = flacer.main(True)
    assert hi == True



if __name__ == "__main__":
    os.environ["CHROME_USR_DIR"] = "/config1"
    test_google_login()