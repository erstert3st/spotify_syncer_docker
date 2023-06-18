import subprocess
import time
import schedule
from threading import Thread
import sys, os
#import flac

# Now do your import

from flac.musicScrapper import Flaccer
# Get the output of the "spotify_sync config list-paths" command and extract the last 7 characters
Spotify_run =False
Flaccer_run = False
def get_flaccs():
    global Flaccer_run
    if Flaccer_run is False:
        Spotify_run  = True
    flaccer = Flaccer() 
    print("startflaccer")
    flaccer.test()
   # flaccer_run = Falsemain


get_flaccs()


#docker run  -it  -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker:/app  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  -v /home/user/Musik/dir:/music -p 5678:5678  -p 9090:9090 -p 9222:9222 spotifysync:0.8.4 /bin/bash