import subprocess
import time
import schedule
from threading import Thread
import sys, os
#import flac

from spotify_sync.cli import SpotifySyncApp
from flac.flacer import Flacer
spotify_run =False
flacer_run = False
def startup_flacer():
    global flacer_run
    if flacer_run is False:
        spotify_run  = True
        flacer = Flacer() 
        print("startflacer")
        flacer.main()
    flacer_run = False

def startup_spotify():
    app = SpotifySyncApp()
    #app.authorize_spotify()
    app.auto()
    
        # try:
        #     subprocess.call(["spotify_sync", "config", "add", "myFirstProfile", "config.json"])
        #     subprocess.call(["spotify_sync", "utils", "authorize-spotify", "--profile", "myFirstProfile"])
        # except:
        #     subprocess.call(["spotify_sync", "config", "remove", "myFirstProfile"])




def startup_spotify():
    global spotify_run
    if spotify_run is False:
        spotify_run  = True
    app = SpotifySyncApp()
    try:
        app = SpotifySyncApp()
        #app.authorize_spotify()
        app.auto()
    except Exception as e:
        print("Error occurred:", e)
        app.authorize_spotify()
    spotify_run = False 
print("startup")


#schedule.every().day.at("16:30").do(daily_task)
schedule.every(1).minute.do(Thread(target=startup_spotify).start())
schedule.every(3).hours.do(Thread(target=startup_flacer).start())
#schedule.every(10).minutes.do(ten_minute_task)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
    get_flaccs()