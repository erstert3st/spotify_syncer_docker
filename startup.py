import subprocess
import time
import schedule
from threading import Thread
import sys, os
#import flac

# Now do your import

from flac.flaccer import Flaccer
# Get the output of the "spotify_sync config list-paths" command and extract the last 7 characters
Spotify_run =False
Flaccer_run = False
def get_flaccs():
    global Flaccer_run
    if Flaccer_run is False:
        Spotify_run  = True
    flaccer = Flaccer() 
    print("startflaccer")
    flaccer.main()
    flaccer_run = False
get_flaccs()

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



def try_download():
    global Spotify_run
    if Spotify_run is False:
        Spotify_run  = True
    try:
        if subprocess.call(["spotify_sync", "run", "auto", "--profile", "myFirstProfile"]) == 0:
            print("Success!")
        else:
            print("Error occurred!")
    except subprocess.CalledProcessError as e:
        print("Error occurred:", e)
    Spotify_run = False 
print("startup")

get_flaccs()

#schedule.every().day.at("16:30").do(daily_task)
schedule.every(1).minute.do(Thread(target=try_download).start())
schedule.every(3).hours.do(Thread(target=try_download).start())
#schedule.every(10).minutes.do(ten_minute_task)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)

if __name__ == '__main__':
    get_flaccs()