FROM python:3.12.7-slim

WORKDIR /app
COPY app.py requirements.txt /app/
COPY server /app/server
COPY web /app/web
RUN apt-get update && apt-get install -y git && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --progress-bar off --no-cache-dir -r /app/requirements.txt && \
    rm -rf /root/.cache/pip

EXPOSE 5000
#  gunicorn --worker-class eventlet -w 1 app:app -b 0.0.0.0:5000
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "app:app", "-b", "0.0.0.0:5000"]