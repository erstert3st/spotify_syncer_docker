FROM debian:bullseye

ENV CHROME_USR_DIR="/root/.config/chromium/"
ENV	wait_time=10

# set display port to avoid crash
ENV DISPLAY=:99
ENV BASE_PATH="/music"
ENV UBLOCK_DIR="/app/flac/uBlock0.chromium"
ENV SELENIUM_CLASS_PATH="/app/flac/selenium_scraper.py"
ENV EMAIL=""
ENV PASSWORD=""
ENV CONFIG_PROFILE="myFirstProfile"
ENV MANUAL_CONFIG_FILE="/app/config.json"
#9090 = spotify 9222-3 debug chrome  5678 debug code
EXPOSE 9090 
EXPOSE 9223
EXPOSE 9222
EXPOSE 5678
RUN apt-get -y update && apt-get install python pip nano chromium ffmpeg xvfb -yqq

RUN mkdir -p /music/MP3 /music/TEMP /app /root/.config/spotify_sync


COPY . /app



WORKDIR /app
RUN chmod +x startup.sh
# install spot_sync from requirements 
RUN pip3 install --no-cache-dir --upgrade pip 
RUN pip3 install --no-cache-dir Poetry 
RUN poetry install
RUN pip3 install -r /app/flac/requirements.txt

#poetry cleanup
RUN pip3 install . 

COPY test/oauth2.py ./usr/local/lib/python3.9/dist-packages/spotipy/oauth2.py
COPY test/oauth2.py ./root/.cache/pypoetry/virtualenvs/spot-sync-9TtSrW0h-py3.9/lib/python3.9/site-packages/spotipy/oauth2.py


RUN apt clean -y
RUN pip cache purge
#RUN poetry cache clear --all
# cmd to run container at start
CMD ["pytest", "py_test.py","-s","-v"]
#CMD ["/bin/bash"]

#
# docker run -it --name spotifysync --rm  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  spotifysync:0.3.1 
# docker run -d --name spotifysync -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  spotifysync:0.3.1
# docker run -it name /bin/bash

# docker run  -it  -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker/flac:/app/flac  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  -p 5678:5678  spotifysync:0.5.20 /bin/bash
# docker run  -it  -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker:/app  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  -v /home/user/Musik/dir:/music -p 5678:5678  spotifysync:0.9.3 /bin/bash
# docker run  -it  -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker:/app  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  -p 5678:5678  spotifysync:0.9.3 /bin/bash
#docker build  -t spotifysync:0.8.2 "." --no-cache
#docker remove: docker rm -f $(docker ps -a -q)

#TODO newer Python version may alpine version
#TODO set env vars in python and remove startuo.sh