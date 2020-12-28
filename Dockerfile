FROM tiangolo/uwsgi-nginx-flask:python3.8
RUN apt-get update
RUN apt-get install -y ca-certificates
ENV STATIC_PATH /app/static
COPY ./requirements.txt requirements.txt
COPY . /app
RUN pip install -r requirements.txt
