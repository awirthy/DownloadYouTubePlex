FROM ghcr.io/linuxserver/baseimage-alpine:3.16

###############################################################################
# YTDL-RSS INSTALL

# COPY root/ /
WORKDIR /config
RUN apk update --no-cache
RUN apk upgrade --no-cache
RUN apk add --update bash
RUN apk --no-cache add ca-certificates python3 py3-pip ffmpeg tzdata nano curl
RUN ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN python3 -m pip install -U yt-dlp
RUN pip install beautifulsoup4
RUN pip install lxml
RUN pip install email-validator
RUN python3 -m pip install requests-html
RUN cp /usr/share/zoneinfo/Australia/Melbourne /etc/localtime
RUN echo "Australia/Melbourne" >  /etc/timezone
RUN wget -O /tmp/DownloadYouTubePlex.tar.gz https://github.com/awirthy/DownloadYouTubePlex/archive/refs/tags/v0.42.0.tar.gz
RUN mkdir -p /opt/DownloadYouTubePlex
RUN tar zxf /tmp/DownloadYouTubePlex.tar.gz -C /opt/DownloadYouTubePlex
RUN echo "#!/bin/sh" >> /etc/periodic/15min/DownloadYouTubePlex
RUN echo "/opt/DownloadYouTubePlex/DownloadYouTubePlex-0.42.0/DownloadYouTubePlex.sh" >> /etc/periodic/15min/DownloadYouTubePlex
RUN chmod 755 /opt/DownloadYouTubePlex/DownloadYouTubePlex-0.42.0/DownloadYouTubePlex.sh
RUN chmod 755 /etc/periodic/15min/DownloadYouTubePlex
CMD ["crond", "-f","-l","8"]
    
###############################################################################
# CONTAINER CONFIGS

ENV EDITOR="nano" \
#ENV TZ="Australia/Melbourne" \
