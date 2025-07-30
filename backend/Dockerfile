FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn python-telegram-bot

COPY . .

# Fix permissions and make script executable
RUN chmod a+x wait-for-db.sh && \
    chown nobody:nogroup wait-for-db.sh

ENTRYPOINT ["/app/wait-for-db.sh"]

RUN mkdir -p /app/card_imgs

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "wsgi:app"]