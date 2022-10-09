FROM python:3.10-buster

COPY . ./

RUN apt-get update && apt-get upgrade -y
RUN apt install sqlite3 -y
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000

CMD python app/app.py
