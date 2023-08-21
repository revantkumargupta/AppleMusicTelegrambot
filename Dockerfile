FROM ubuntu:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=America/Los_Angeles
RUN apt-get update

RUN apt-get -qq update --fix-missing
RUN apt-get -qq install -y git wget curl busybox python3 python3-pip locales ffmpeg aria2 yt-dlp

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


COPY bin/MP4Box.deb /usr/bin/
COPY bin/mp4decrypt /usr/bin/


RUN chmod +x /usr/bin/MP4Box.deb
RUN chmod +x /usr/bin/mp4decrypt


RUN apt-get install -y gpac

CMD ["bash", "start.sh"]
