FROM docker.io/python:3.12

WORKDIR /

# --- [Install python and pip] ---
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip git
COPY . /

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

ENV GUNICORN_CMD_ARGS="--workers=3 --bind=0.0.0.0:8101"

# This was 8087 before deployment changes
EXPOSE 8101

# Define environment variable
ENV FLASK_ENV=development

CMD [ "gunicorn", "main:app" ]
