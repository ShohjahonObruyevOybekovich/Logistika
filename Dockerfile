FROM python:3.12.3-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY r.txt /usr/src/app/r.txt
RUN pip install -r r.txt

COPY entrypoint.sh /usr/src/app/entrypoint.sh
COPY . /usr/src/app/

# ENTRYPOINT ["/usr/src/app/entrypoint.sh"]