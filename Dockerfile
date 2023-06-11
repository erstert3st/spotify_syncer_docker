FROM ultrafunk/undetected-chromedriver:latest

#Set Environment Vars for docker
ENV arl=xxx 
ENV	spot_id=x  
ENV	spot_secret=x 
ENV	spot_username=**None** 
#minute wait 
ENV	wait_time=10
    #	DiscordBotToken = **None** \ 
	#CHANNEL = **None** 
ENV CHROME_USR_DIR="/root/.config/google-chrome/"
# set display port to avoid crash
ENV DISPLAY=:99
ENV BASEBATH=/musik/MP3

EXPOSE 9090
EXPOSE 5678
RUN apt-get -y update && apt-get install nano -yqq

# RUN CHROMEVER=$(google-chrome --product-version | grep -o "[^\.]*\.[^\.]*\.[^\.]*") && \
#     DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROMEVER") && \
#     wget -q --continue -P /chromedriver "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
#     unzip /chromedriver/chromedriver* -d /chromedriver

# install chromedriver
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/




RUN mkdir -p  /musik/MP3
RUN mkdir /app
RUN mkdir /root/.config/spotify_sync -p

#COPY config.json /app
#COPY startup.sh /app
COPY . /app

WORKDIR /app
RUN chmod +x startup.sh
# install spot_sync from requirements 
RUN pip3 install --no-cache-dir --upgrade pip 
RUN pip3 install --no-cache-dir Poetry 
RUN poetry install
RUN pip3 install -r /app/flac/requirements.txt
#poetry cleanup

#&& pip install -U spot_sync --no-cache-dir 
#RUN pip3 install -U spot_sync --no-cache-dir 
#RUN pip3 uninstall  spot_sync  -y
RUN pip3 install . 
RUN apt clean -y
RUN pip cache purge
# cmd to run container at start
#CMD ["/bin/bash", "/app/startup.sh"]
CMD ["/bin/bash"]

# docker build  -t spotifysync:0.3.6 "." --no-cache
# docker run -it --name spotifysync --rm  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  spotifysync:0.3.1 
# docker run -d --name spotifysync -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  spotifysync:0.3.1
# docker run -it name /bin/bash

# docker run  -it  -v /home/user/Schreibtisch/spotDocker/spotify_sync_docker/flac:/app/flac  -v /home/user/Schreibtisch/tempp:/root/.config/spotify_sync  -p 5678:5678  spotifysync:0.5.20 /bin/bash

#TODO newer Python version may alpine version
#TODO set env vars in python and remove startuo.sh