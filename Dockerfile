FROM python:3.6.8
# RUN apk add g++ gcc libxml2-dev libxslt-dev musl-dev linux-headers
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt
ADD . /app