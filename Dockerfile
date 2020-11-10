FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /uniclub_mobile
RUN mkdir /uniclub_mobile/staticfiles
RUN mkdir /uniclub_mobile/media
WORKDIR /uniclub_mobile
ADD requirements.txt /uniclub_mobile/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /uniclub_mobile/

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait