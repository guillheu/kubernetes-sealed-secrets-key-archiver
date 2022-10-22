FROM python:alpine3.16

RUN pip install kubernetes
RUN pip install python-gnupg

RUN apk --no-cache add gnupg

COPY src src

RUN chmod +x /src/*

ENTRYPOINT ["src/main.py"]