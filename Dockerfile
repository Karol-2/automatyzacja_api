FROM python:3.8

WORKDIR /app

COPY api/main.py /app/

COPY api/test-integration.py /app/

COPY api/requirements.txt /app/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]