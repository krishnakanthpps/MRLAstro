# MRLAstro

Flask based Sayana Horoscope generator.

## Installation

```
pip3 install -r requirements.txt 
export FLASK_APP=app.py
flask run
```

## Dockerized 

Create image and run container

```
docker build -t mrlastro.test 

docker container logs -f mrlastro.test
```
