FROM python:3.8
WORKDIR /projet-GLO-4035
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD python main.py