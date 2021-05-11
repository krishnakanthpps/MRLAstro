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
./redo-docker.sh

docker container logs --tail -f mrlastro.test
```

Browse to http://localhost:8080
