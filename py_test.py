import pytest
import os 
import shutil

from flac.flacer import Flacer
from flac.selenium_scraper import selenium_scraper 
#from spotify_sync.cli import SpotifySyncApp
from spotify_sync.cli import SpotifySyncApp
from syncer.syncer import Syncer

#app = SpotifySyncApp()
#app.sync_spotify()


# def test_login():
#     print("start test:")
def test_env_vars():
    print("start test: def test_env_vars():")
    #Todo: add if folder exist 
    assert  len(os.getenv("DISPLAY","")) >= 1
    assert  len(os.getenv("BASE_PATH","")) >= 1
    assert  len(os.getenv("UBLOCK_DIR","")) >= 1
    assert  len(os.getenv("SELENIUM_CLASS_PATH","")) >= 1
    assert  len(os.getenv("CHROME_USR_DIR","")) >= 1
    assert  len(os.getenv("EMAIL","")) >= 1
    assert  len(os.getenv("PASSWORD","")) >= 1
    assert  len(os.getenv("CONFIG_PROFILE","")) >= 1
    assert  len(os.getenv("MANUAL_CONFIG_FILE","")) >= 1
    assert  len(os.getenv("CLIENT_SECRET_FILE","")) >= 1
    assert  len(os.getenv("1CHROMEDRIVER_PATH","")) >= 1

# def test_file_exists():
#     print("start test: def test_file_exists():")
#     client_secret = os.getenv("CLIENT_SECRET_FILE","syncer/client_secret.json")  # Replace with the actual file path
#     config_dile_spotify = os.getenv("MANUAL_CONFIG_FILE","config.json")  # Replace with the actual file path
#     assert os.path.isfile(client_secret), f"File '{client_secret}' does not exist"
#     assert os.path.isfile(config_dile_spotify), f"File '{config_dile_spotify}' does not exist"

def test_login_spotify():
    print("start test: def test_login_spotify():")
    
    app = SpotifySyncApp()
   # os.environ['CONFIG_PROFILE'] = 'myFirstProfile'
   # os.environ['MANUAL_CONFIG_FILE'] = '/home/user/Schreibtisch/spotDocker/spotify_sync_docker/config.json'
    # Call the sync_spotify() function
    app.authorize_spotify()
    assert True == True

def test_copy():
    print("start test: def test_copy():")
    base_path = os.getenv("BASE_PATH","/home/user/Musik/music")
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
    print("start test: test_flac_working")
    flacer = Flacer()
    assert  flacer.check_flac("flac_test_files/working.flac") == True

def test_flac_not_working(): #
    print("start test: test_flac_not_working")
    flacer = Flacer()
    assert  flacer.check_flac("flac_test_files/not_working.flac") == False

def test_google_login():
    print("start test: test_google_login")
    selenium = selenium_scraper()
    googleLink = selenium.login_google()
    print(googleLink)
    assert googleLink.startswith("https://myaccount.google.com") 

def test_check_browser():
    print("start test: test_check_browser")
    selenium = selenium_scraper()
    redirect_url = selenium.check_browser()
    assert redirect_url == True

def test_syncer_file_check():
    print("start test: test_syncer_file_check")
    Syncer.check_for_new_files()
    file_path = os.getenv("BASE_PATH","/home/user/Musik/music") + "/file_list.txt"
    assert os.path.isfile(file_path), f"File '{file_path}' does not exist"


def test_download_flac():
    flacer = Flacer() #Todo add BasePath after test than list files and than remove file 
    hi = flacer.main()
   # hi = flacer.main(True)
    assert hi == True



if __name__ == "__main__":
   # os.environ["CHROME_USR_DIR"] = "/config1"
    #os.environ["MANUAL_CONFIG_FILE"] = "/home/user/Schreibtisch/spotDocker/spotify_sync_docker/config.json"
    #os.environ["CONFIG_PROFILE"] = "myFirstProfile"
    test_check_browser()
