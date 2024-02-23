FROM python:3.11
WORKDIR /app
COPY wait-for-it.sh entrypoint.sh ./
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["./entrypoint.sh"]