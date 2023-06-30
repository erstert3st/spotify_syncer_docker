import subprocess
import time
import schedule
from threading import Thread
import sys, os
import pytest

from spotify_sync.cli import SpotifySyncApp
from flac.flacer import Flacer
from syncer.syncer import Syncer

spotify_run =False
flacer_run = False

def build_flacer():
    flacer = Flacer() 
    flacer.build()
    print("login flacer done")

def build_spotify():
    app = SpotifySyncApp()
    app.authorize_spotify()
    print("logins spotify done")

def sync_google_drive(check_file_changed):
    print("google drive sync start:")
    Syncer.main_syncer(check_file_changed)
    print("google drive sync Done!")
def startup_flacer():
    global flacer_run
    if flacer_run is False:
        flacer_run  = True   
        try:
            flacer = Flacer() 
            print("startflacer")
            flacer.main()
        except Exception as e:
            print("Error occurred:", e)
            print("flaccer error")
    flacer_run = False

def startup_spotify():
    global spotify_run
    if spotify_run is False:
        spotify_run  = True
        app = SpotifySyncApp()
        try:
            #app.authorize_spotify()
            app.authorize_spotify() #Todo do you need it ? 
            try:
                app.auto()
                if Syncer.check_for_new_files() is True:
                    print("new Files found start flaccer")
                    Flacer.main()
            except:app.authorize_spotify()
        except Exception as e:
            print("Error occurred:", e)
            print("fail add spotify")
            
        spotify_run = False 

def run_test():
    pytest.main([ '-s', 'py_test.py'])


def main():
    if len(os.getenv("RUN_TEST","")) >= 1:run_test()
    #sync_google_drive()
    build_flacer()
    build_spotify()
    print("startup")
    #Todo : Make flacer as modul 
    #Todo : all other Todos :P
    #schedule.every().day.at("16:30").do(daily_task)
    schedule.every(5).minute.do(Thread(target=startup_spotify()).start())
    schedule.every(3).hours.do(Thread(target=startup_flacer()).start())
   # schedule.every(12).hours.do(Thread(target=sync_google_drive()).start())
   # schedule.every(24).hours.do(Thread(target=sync_google_drive(False)).start())
    #schedule.every(10).minutes.do(ten_minute_task)

    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    main()
    #  os.environ["CONFIG_PROFILE"] = "myFirstProfile"
    #  os.environ["MANUAL_CONFIG_FILE"] = "/home/user/Schreibtisch/spotDocker/spotify_sync_docker/config.json"
    #  build_spotify()