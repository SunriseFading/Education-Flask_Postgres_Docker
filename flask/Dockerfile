FROM python:3.8.3

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt
RUN pip install uwsgi

CMD ["/usr/local/bin/uwsgi", "app.ini"]