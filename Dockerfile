FROM python:3.6.8-alpine
COPY . /app
WORKDIR /app
RUN apk add g++ gcc libxslt-dev musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8420