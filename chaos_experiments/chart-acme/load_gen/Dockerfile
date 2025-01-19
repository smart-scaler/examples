FROM python:3.10

# Set destination for COPY
WORKDIR /app

COPY requirements.txt heartbeat.py sinusoidal.py constant_load_with_retries.py run.sh ./

RUN pip install -r requirements.txt

CMD ["bash", "run.sh"]