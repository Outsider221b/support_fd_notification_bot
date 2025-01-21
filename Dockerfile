FROM python:3.9-alpine3.16

COPY requirements.txt /requirements.txt
COPY app.py /bot/app.py
COPY settings.py /bot/settings.py

WORKDIR /bot

RUN pip install -r /requirements.txt

RUN adduser --disabled-password webapp-user

USER webapp-user

CMD ["python", "app.py"]