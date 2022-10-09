FROM python:3.10-buster

COPY . ./

ENV FLASK_APP=app/app.py
ENV FLASK_RUN_HOST=0.0.0.0

RUN apt-get update && apt-get upgrade -y
RUN apt install sqlite3 -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app/app.py
