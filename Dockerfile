#FROM navikey/raspbian-buster
FROM debian:stable

ENV CHROME_USR_DIR="/config"
ENV	wait_time=10

ENV DISPLAY=:99 
ENV BASE_PATH="/music"
ENV UBLOCK_DIR="/app/flac/ublock_arm/uBlock-Origin"
ENV SELENIUM_CLASS_PATH="/app/flac/selenium_scraper.py"
ENV EMAIL="downlod3rmusik@gmail.com"
ENV PASSWORD="123456789L0LxD"
ENV CONFIG_PROFILE="myFirstProfile"
ENV MANUAL_CONFIG_FILE="/app/config.json"
ENV CLIENT_SECRET_FILE="/app/syncer/client_secret.json"
ENV CHROMEDRIVER_PATH="/usr/local/bin/chromedriver"
ENV CHROME_PATH="/usr/bin/chromium"
ENV RUN_TEST="True"
#9090 = spotify 9222-3 debug chrome  5678 debug code
EXPOSE 9090 
EXPOSE 9223
EXPOSE 9222
EXPOSE 5678

#Todo make universal chromedriver 
# Install deb
RUN apt-get update && apt-get install  --no-install-recommends -yqq nano ffmpeg chromium python3-dev pip unzip wget gcc xvfb
RUN mkdir -p /music/MP3 /music/TEMP /app /root/.config/spotify_sync /config

# SETUP Python 3.9 
WORKDIR /app
#Instal chromedriver only on AARCH !
RUN if [ "$(uname -m)" = "aarch64" ]; then \ 
    wget  --no-check-certificate -O chromedriver.zip https://github.com/electron/electron/releases/download/v25.3.0/chromedriver-v25.3.0-linux-arm64.zip &&\ 
    unzip chromedriver.zip && \
    chmod +x chromedriver && \ 
    mv chromedriver  /usr/local/bin && \
    rm -rf *; fi


COPY . /app
WORKDIR /app

# install pip requirements 
RUN pip3 install --no-cache-dir --upgrade pip  --break-system-packages
RUN pip3 install -r /app/flac/requirements.txt --no-cache-dir --break-system-packages
RUN python3 --version
# replace interactive spotify login 
RUN rm /usr/local/lib/python3.11/dist-packages/spotipy/oauth2.py -rf
COPY spotify_replace/oauth2.py /usr/local/lib/python3.11/dist-packages/spotipy/oauth2.py
WORKDIR /app
#cleanup
RUN apt clean -y
RUN pip cache purge

CMD ["python3", "startup.py"]
#CMD ["python3", "py_test.py","-s","-v"]

#docker run -it   -v /mnt/ssd/media/config/spotify_sync/profiles:/root/.config/spotify_sync   -v /mnt/ssd/media/config/spotify_sync/cache:/root/.local/share/spotify_sync   -v /mnt/ssd/media/music/music:/music   -p 5678:5678   -p 9090:9090 -v /home/pi/builder/spotify_sync_docker:/app -e CHROME_USR_DIR="/usr/bin/chromium_profile"    spotifysyncer:2.0.0 /bin/bash
#docker remove all container : docker rm -f $(docker ps -a -q)
#TODO newer Python version may alpine version