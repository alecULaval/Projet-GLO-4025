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
COPY resources/intersections_only_coords.csv intersections_only_coords.csv
COPY resources/json_toronto_reformated.json json_toronto_reformated.json
COPY resources/routes.json routes.json
COPY resources/restos_cornwall_formatted.json restos_cornwall_formatted.json


RUN pip install -Ur requirements.txt
CMD python app.py