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
        Thread(target=start_flacer()).start()
def startup_spotify():
    global spotify_run
    if spotify_run is False:
        Thread(target=start_spotify()).start()
def start_flacer():
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


def start_spotify():
    global spotify_run
    if spotify_run is False:
        spotify_run  = True
        app = SpotifySyncApp()
        try:
            #app.authorize_spotify()
            app.authorize_spotify() #Todo do you need it ? 
            try:
                output = subprocess.check_output("spotify_sync run auto --profile myFirstProfile", shell=True, cwd="/")
                print(output.decode())
                if Syncer.check_for_new_files() is True:
                    print("new Files found start flaccer")
                    Flacer.main()
            except:app.authorize_spotify()
        except Exception as e:
            print("Error occurred:", e)
            print("fail add spotify")
            
        spotify_run = False 

def run_test():
    pytest.main([ 'py_test.py','-s','-k' ,'(not login) and (not download_flac)'])


def main():
    if len(os.getenv("RUN_TEST","")) >= 1:
        run_test()
        exit(0)
    build_flacer()
    build_spotify()
    print("startup")
    #Todo : Make flacer as modul 
    #Todo : all other Todos :P
    #schedule.every().day.at("16:30").do(daily_task)
    schedule.every(1).minutes.do(startup_spotify)
    schedule.every(3).hours.do(startup_flacer)
   # schedule.every(24).hours.do(Thread(target=sync_google_drive(False)).start())
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(1)
if __name__ == "__main__":
    #build_spotify()
    #os.environ["CONFIG_PROFILE"] = "myFirstProfile"
    #os.environ["MANUAL_CONFIG_FILE"] = "/home/user/Dokumente/private_git2/spotify_syncer_docker_old/config.json"
    #os.environ["EMAIL"] = "downlod3rmusik@gmail.com"
   # os.environ["PASSWORD"] = "123456789KkL0LLOLxD"
   main()
   # build_flacer()
    #schedule.every(1).minute.do(Thread(target=startup_flacer()).start)
