FROM python:3.8

ADD . /compose_flask
WORKDIR /compose_flask
RUN pip install -r requirements.txt
COPY . /compose_flask
CMD python app.py