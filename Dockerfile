FROM python:3.6.9-buster

RUN mkdir /app
COPY ./  /app
COPY entrypoint.sh /app/
RUN pip install -r /app/requirements.txt


CMD ["python", "/app/app.py"]
