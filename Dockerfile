FROM python:3.9-alpine

WORKDIR /app

LABEL maintainer="Shahid Kamal"
LABEL version="1.0.0"

# required env
ENV APP_ID=
ENV APP_HASH=
# can mount /app/config to keep the session file around
VOLUME [ "/app/config" ]

# prepare env
RUN apk add --no-cache gcc g++ make libffi-dev openssl-dev
# install deps
COPY requirement.txt requirement.txt
RUN pip install -r requirement.txt

#copy and start the script
COPY . .
CMD [ "python", "main.py" ]