FROM dorowu/ubuntu-desktop-lxde-vnc
MAINTAINER evanesoeric <evanesoteric@tutamail.com>


USER root
WORKDIR /root


# set to 1 as required
RUN export DISPLAY=:1


RUN apt-get update
RUN apt-get full-upgrade -y
RUN apt-get autoremove -y
RUN apt-get install -y apt-utils
RUN apt-get install -y \
  gnupg \
  dirmngr \
  iputils-ping \
  rsync \
  curl \
  nano \
  sed \
  wget \
  ntp \
  htop \
  iotop \
  vnstat \
  sysstat \
  psmisc \
  libcurl4-gnutls-dev \
  lsof \
  strace \
  python3 \
  python3-dev \
  python3-setuptools \
  python3-pip \
  python3-virtualenv \
  python3-requests \
  python3-urllib3 \
  alsa-utils


# install firefox
RUN cd /tmp
RUN wget https://ftp.mozilla.org/pub/firefox/releases/73.0.1/linux-x86_64/en-US/firefox-73.0.1.tar.bz2
RUN tar xvf firefox*.tar.bz2
RUN mv firefox/ /opt
RUN ln -f -s /opt/firefox/firefox /usr/bin/firefox
RUN rm firefox*.tar.bz2

# install gecko driver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
RUN tar -xzf geckodriver*.tar.gz
RUN chmod +x geckodriver
RUN mv geckodriver /usr/bin/
RUN rm geckodriver*.tar.gz



COPY ./redrocket .
COPY ./requirements.txt .


RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
