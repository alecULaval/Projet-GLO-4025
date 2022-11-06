FROM python:3.8

# ADD . /app
WORKDIR /app
COPY requirements.txt requirements.txt
COPY populate_neo4j.py populate_neo4j.py
COPY .env .env
COPY populate_mongodb.py populate_mongodb.py
COPY app.py app.py
COPY Restaurant.py Restaurant.py
COPY resources/json_cornwall_reformated.json resources/json_cornwall_reformated.json
COPY resources/routes.json resources/routes.json
COPY resources/restos_cornwall_formatted.json resources/restos_cornwall_formatted.json
COPY resources/intersections.json resources/intersections.json


RUN pip install -Ur requirements.txt
CMD python app.py