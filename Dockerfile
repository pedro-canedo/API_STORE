FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .

RUN chmod +x entrypoint.sh

RUN apt-get update && apt-get install -y postgresql-client

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh


ENTRYPOINT ["/app/entrypoint.sh"]
