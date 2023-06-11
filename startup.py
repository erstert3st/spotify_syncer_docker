import subprocess
import time
import schedule
import threading
import sys, os
import flac
# Now do your import

from flac.musicScrapper import Flaccer
# Get the output of the "spotify_sync config list-paths" command and extract the last 7 characters
def startup():
    # Check if the output is "-----" = means no config 
    #Todo check if config is valid ? 
    #Todo download folder
    #Todo Check if second captcha 
    #Test config save
    #Todo ARM 
    #cleanup
    #DONE
    print("start_")
    output = subprocess.check_output(["spotify_sync", "config", "list"]).decode().splitlines()
    #print(len(output[))
    if len(output) < 4 or output[4] != "myFirstProfile":
        print("no config found")
        subprocess.call(["spotify_sync", "config", "add", "myFirstProfile", "config.json"])
        subprocess.call(["spotify_sync", "utils", "authorize-spotify", "--profile", "myFirstProfile"])
    else:
        #spotify_sync stats playlists
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

print("startup")
startup()
#schedule.every().day.at("16:30").do(daily_task)
schedule.every(1).hours.do(hourly_task)
schedule.every(3).hours.do(five_hour_task)
#schedule.every(10).minutes.do(ten_minute_task)
