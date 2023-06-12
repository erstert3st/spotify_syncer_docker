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
    #Todo Check if second captcha 
    #Test config save -> #Todo: Cache Auth to file ? 
    # if stuck try Video Downloader
    #Todo ARM 
    #cleanup
    #DONE
    print("start_")
    output = subprocess.check_output(["spotify_sync", "config", "list"]).decode()
    #print(len(output[))
    print(len(output)) #6
    #Todo check if config/cookie is valid
    #Todo may add webinsert so you dont need except into container
    #if len(output) < 4:# or output[4] != "myFirstProfile":
    if not  "myFirstProfile" in output:
        print("no config found")
        try:
            subprocess.call(["spotify_sync", "config", "add", "myFirstProfile", "config.json"])
            subprocess.call(["spotify_sync", "utils", "authorize-spotify", "--profile", "myFirstProfile"])
        except:
            subprocess.call(["spotify_sync", "config", "remove", "myFirstProfile"])

    else:
        #spotify_sync stats playlists
        print("config ok")

def five_hour_task():
    flaccer = Flaccer() 
    flaccer.test()

def try_download():
    try:
        if subprocess.call(["spotify_sync", "run", "auto", "--profile", "myFirstProfile"]) == 0:
            print("Success!")
        else:
            print("Error occurred!")
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)

print("startup")

five_hour_task()

#schedule.every().day.at("16:30").do(daily_task)
schedule.every(1).minute.do(try_download)
schedule.every(3).hours.do(five_hour_task)
#schedule.every(10).minutes.do(ten_minute_task)
