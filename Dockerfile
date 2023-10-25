FROM python:3.8

RUN mkdir /app

WORKDIR /api

COPY main.py /app/

COPY test-integration.py /app/

COPY requirements.txt /app/

RUN pip install -r requirements.txt

CMD ["python", "main.py"]