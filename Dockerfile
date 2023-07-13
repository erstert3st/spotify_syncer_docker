#FROM navikey/raspbian-buster
FROM navikey/raspbian-buster
#FROM debian:stable

ENV CHROME_USR_DIR="/config"
ENV	wait_time=10

# set display port to avoid crash
ENV DISPLAY=:99
ENV BASE_PATH="/music"
ENV UBLOCK_DIR="/app/flac/ublock_arm/uBlock-Origin"
ENV SELENIUM_CLASS_PATH="/app/flac/selenium_scraper.py"
ENV EMAIL="downlod3rmusik@gmail.com"
ENV PASSWORD="123456789L0LxD"
ENV CONFIG_PROFILE="myFirstProfile"
ENV MANUAL_CONFIG_FILE="/app/config.json"
ENV CLIENT_SECRET_FILE="/app/syncer/client_secret.json"
ENV CHROMEDRIVER_PATH="/usr/bin/chromedriver"
ENV RUN_TEST="True"
#9090 = spotify 9222-3 debug chrome  5678 debug code
EXPOSE 9090 
EXPOSE 9223
EXPOSE 9222
EXPOSE 5678

#RUN apt-get update && apt-get install nano ffmpeg python3-full pip chromium xvfb curl --no-install-recommends -yqq
RUN apt-get update 
RUN apt-get upgrade -yqq
RUN apt-get dist-upgrade -yqq
# Install deb
RUN  apt-get install  --no-install-recommends -yqq nano ffmpeg 
RUN apt-get install   --no-install-recommends -yqq  chromium xvfb gcc  
RUN mkdir -p /music/MP3 /music/TEMP /app /root/.config/spotify_sync /config

# SETUP Python 3.9 
WORKDIR /app
# Install necessary dependencies
RUN apt-get update && apt-get install -y build-essential  wget zlib1g-dev  libffi-dev  libssl-dev libsqlite3-dev
# Download Python source code
RUN wget https://www.python.org/ftp/python/3.9.15/Python-3.9.15.tgz && tar -xvf Python-3.9.15.tgz
# Build and install Python
RUN cd Python-3.9.15 && ./configure --enable-optimizations && make && make install
# Clean up downloaded files
RUN rm -rf Python-3.9.15 Python-3.9.15.tgz




COPY . /app
WORKDIR /app


# install spot_sync from requirements 
#Todo remove unnecesarry installs
RUN pip3 install --no-cache-dir --upgrade pip  
RUN pip3 install -r /app/flac/requirements.txt --no-cache-dir 
#RUN pip3.9 install . --no-cache-dir
#RUN poetry install
RUN apt-get update && apt-get install  --no-install-recommends -yqq chromium-chromedriver

#RUN pip3 install . 
WORKDIR /

#RUN rm /usr/local/lib/python3.9/site-packages/spotipy/oauth2.py -rf
#COPY test/oauth2.py /usr/local/lib/python3.11/dist-packages/spotipy/oauth2.py
#COPY test/oauth2.py  /usr/local/lib/python3.9/site-packages/spotipy/oauth2.py
#COPY test/oauth2.py ./root/.cache/pypoetry/virtualenvs/spot-sync-9TtSrW0h-py3.9/lib/python3.9/site-packages/spotipy/oauth2.py
WORKDIR /app
#poetry cleanup
RUN apt clean -y
RUN pip3.9 cache purge
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
#docker run -it -v /home/pi/builder/spotify_sync_docker:/app  navikey/raspbian-bullseye
#TODO newer Python version may alpine version
#TODO set env vars in python and remove startuo.sh