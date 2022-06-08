FROM dockerhub.ir/python:3.6.9

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/myserver

WORKDIR /code

COPY HTTP_server.py /code/

CMD ["python","HTTP_server.py"]
