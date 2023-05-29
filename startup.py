import subprocess
import time
import schedule
import threading
import sys, os
sys.path.append('/home/user/Schreibtisch/spotDocker/spotify_sync_docker/flac')
# Now do your import
from musicScrapper import Flaccer
# Get the output of the "spotify_sync config list-paths" command and extract the last 7 characters
def startup():
    # Check if the output is "-----" = means no config 
    output = subprocess.check_output(["spotify_sync", "config", "list-paths"]).decode().splitlines()[-1][-7:]
    if output == "-----":
        subprocess.call(["spotify_sync", "config", "add", "myFirstProfile", "config.json"])
        subprocess.call(["spotify_sync", "utils", "authorize-spotify", "--profile", "myFirstProfile"])
    else:
        print("config ok")

def five_hour_task():
    flaccer = Flaccer() 
    flaccer.main()

def hourly_task():
    try:
        if subprocess.call(["spotify_sync", "run", "auto", "--profile", "myFirstProfile"]) == 0:
            print("Success!")
        else:
            print("Error occurred!")
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)


#schedule.every().day.at("16:30").do(daily_task)
schedule.every(1).hours.do(hourly_task)
schedule.every(3).hours.do(five_hour_task)
#schedule.every(10).minutes.do(ten_minute_task)