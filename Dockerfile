FROM python:3.8

# ADD . /app
WORKDIR /app
COPY requirements.txt requirements.txt
COPY populate_neo4j.py populate_neo4j.py
COPY .env .env
COPY mongodb.py mongodb.py
COPY neo4jdb.py neo4jdb.py
COPY app.py app.py
COPY Restaurant.py Restaurant.py
COPY resources/restaurant_dataset.csv restaurant_dataset.csv


RUN pip install -Ur requirements.txt
CMD python app.py