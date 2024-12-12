# use Python Image
FROM python:3.12

# work dir
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app
#COPY ./.env.example /app/

#ENV SQLITE_DATABASE=/app/database.db
#RUN mkdir -p /data && touch /data/database.db


# expose interface 8000
EXPOSE 8000

# put on
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

