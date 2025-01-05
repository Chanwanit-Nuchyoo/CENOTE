FROM python:3.9-alpine

RUN apk add --no-cache \
  tcl-dev \
  tk-dev \
  libx11 \
  && apk add --no-cache --virtual .build-deps build-base \
  && pip install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Create entrypoint.sh script to handle migrations and superuser creation
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the default command to run migrations, create superuser, and then run the server
CMD ["/entrypoint.sh"]
