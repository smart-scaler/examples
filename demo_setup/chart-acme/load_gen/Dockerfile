FROM python:3.10

# Set destination for COPY
WORKDIR /app

COPY requirements.txt heartbeat.py run.sh ./

RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]