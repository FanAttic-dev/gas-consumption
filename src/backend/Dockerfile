FROM ubuntu:22.04

RUN apt-get update \
    && apt-get -y install tesseract-ocr \
    && apt-get install -y python3 python3-distutils python3-pip \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 --no-cache-dir install --upgrade pip \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

RUN flask db init

CMD ["uwsgi", "wsgi.ini"]