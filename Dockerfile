FROM python:3.7-alpine

WORKDIR /app
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc libffi-dev openssl-dev musl-dev linux-headers
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5000
COPY src/ .

CMD [ "sh", "/app/entrypoint.sh" ]
