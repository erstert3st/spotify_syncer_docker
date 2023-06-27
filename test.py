import subprocess
import time
import schedule
from threading import Thread
import sys, os
#import flac

# Now do your import

from flac.flacer import Flacer
# Get the output of the "spotify_sync config list-paths" command and extract the last 7 characters
Spotify_run =False
Flacer_run = False
def get_flaccs():
    global Flacer_run
    if Flacer_run is False:
        Spotify_run  = True
    flacer = Flacer() 
    print("startflacer")
    flacer.test()
   # flacer_run = Falsemain


get_flaccs()


#docker run  -it  -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker:/app  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  -v /home/user/Musik/music:/music -p 5678:5678  -p 9090:9090 -p 9222:9222 spotifysync:0.8.4 /bin/bash