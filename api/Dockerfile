# To use this for local development:
# First build the image:
#
#   $ docker build -t valuation-tool-api:latest .
#

FROM ubuntu:18.04

MAINTAINER Dustin Olley <dolleyj@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    apache2 libapache2-mod-wsgi curl \
    python3.6 python3-pip python3-dev build-essential \
    python3-flask python3-flask-login

# curl --tlsv1 -vk https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN mkdir /export 

WORKDIR /export/api

# RUN pip install --upgrade pip==10.0.1 
# RUN pip install -Iv Flask==0.12.2 \
#     && pip install -Iv Flask-Cors==3.0.3 \
#     && pip install -Iv requests==2.12.4

# TODO After successful image build/running, need to confirm versions

RUN pip3 install Flask \
    && pip3 install Flask-Cors \
    && pip3 install requests \
    && pip3 install pandas \
    && pip3 install numpy



CMD ["python3", "app.py"]
# COPY ./valuation-tool-apache2.conf /etc/apache2/sites-available/valuation-tool-apache2.conf

# RUN a2enmod proxy
# RUN a2enmod proxy_http

# RUN a2dissite 000-default.conf
# RUN a2ensite valuation-tool-apache2.conf

# EXPOSE 80

# CMD /usr/sbin/apache2ctl -D FOREGROUND
