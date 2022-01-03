FROM python:3.9-alpine3.15 AS base

FROM base as builder
RUN mkdir /install
COPY ./requirements.txt /requirements.txt
RUN apk add --update postgresql-client postgresql-dev gcc python3-dev musl-dev
WORKDIR /install
RUN pip install --prefix=/install -r /requirements.txt


FROM base
LABEL name Fredrik Andersson

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

COPY --from=builder /install /usr/local
RUN apk --no-cache add libpq
RUN mkdir /app
COPY ./app /app
WORKDIR /app

RUN adduser -D user
USER user
