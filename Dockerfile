FROM python:3.6-slim

RUN mkdir /liquidnet

WORKDIR /liquidnet

ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

EXPOSE 8000

#ENV FLASK_APP=run.py

CMD python3 -m unittest discover; python3 run.py