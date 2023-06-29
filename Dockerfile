FROM debian:stable-slim

ENV CHROME_USR_DIR="/config"
#ENV CHROME_USR_DIR="/root/.config/chromium/"
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
ENV CLIENT_SECRET_FILE="/app/syncer/client_secret.json"
ENV RUN_TEST="True"
#9090 = spotify 9222-3 debug chrome  5678 debug code
EXPOSE 9090 
EXPOSE 9223
EXPOSE 9222
EXPOSE 5678

#RUN apt-get update && apt-get install nano ffmpeg python3-full pip chromium xvfb curl --no-install-recommends -yqq
RUN apt-get update && apt-get install nano ffmpeg python3-full pip chromium xvfb curl  --no-install-recommends -yqq
RUN mkdir -p /music/MP3 /music/TEMP /app /root/.config/spotify_sync /config

COPY . /app
WORKDIR /app


# install spot_sync from requirements 
#Todo remove unnecesarry installs
RUN pip3 install --no-cache-dir --upgrade pip  --break-system-packages
RUN pip3 install -r /app/flac/requirements.txt --no-cache-dir --break-system-packages
RUN pip3 install . --no-cache-dir --break-system-packages
#RUN poetry install

#poetry cleanup
#RUN pip3 install . 
WORKDIR /

RUN rm /usr/local/lib/python3.11/dist-packages/spotipy/oauth2.py -rf
#COPY test/oauth2.py /usr/local/lib/python3.11/dist-packages/spotipy/oauth2.py
COPY /test/oauth2.py  /usr/local/lib/python3.11/dist-packages/spotipy/oauth2.py
#COPY test/oauth2.py ./root/.cache/pypoetry/virtualenvs/spot-sync-9TtSrW0h-py3.9/lib/python3.9/site-packages/spotipy/oauth2.py
WORKDIR /app

RUN apt clean -y
RUN pip cache purge
#RUN python3 -c 'import startup; startup.build_flacer()'
#RUN python3 -c 'import startup; startup.build_spotify()'
#RUN poetry cache clear --all
# cmd to run container at start
CMD ["python3", "startup.py"]
#CMD ["python3", "py_test.py","-s","-v"]
#CMD ["/bin/bash"]


#
#TODO newer Python version may alpine version
#TODO set env vars in python and remove startuo.sh




# docker run -it name /bin/bash

# docker run  -it  -v /home/user/Musik/configs/chrome_user_dir:/root/.config/chromium/ -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker:/app  -v /home/user/Musik/configs/spotify_sync:/root/.config/spotify_sync -v /home/user/Musik/music:/music -e EMAIL=downlod3rmusik@gmail.com -e PASSWORD=123456789987654321L0L  -p 5678:5678  spotifysync:1.0.88 /bin/bash



#docker run  -it   -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker:/app  -v /home/user/Musik/configs/spotify_sync/profiles:/root/.config/spotify_sync -v /home/user/Musik/configs/spotify_sync/cache:/root/.local/share/spotify_sync -v /home/user/Musik/music:/music -p 5678:5678  spotifysync:3.0.0 /bin/bash
#docker build  -t spotifysync:0.8.2 "." --no-cache
#docker remove: docker rm -f $(docker ps -a -q)
#
#TODO newer Python version may alpine version
#TODO set env vars in python and remove startuo.sh