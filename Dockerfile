FROM python:3.9-alpine3.15 AS base

FROM base as builder
RUN mkdir /install
RUN apk add --update postgresql-client postgresql-dev gcc python3-dev \
                     musl-dev jpeg-dev zlib zlib-dev
WORKDIR /install
COPY ./requirements.txt /requirements.txt
RUN pip install --prefix=/install -r /requirements.txt
# RUN pip install -r /requirements.txt

# /usr/lib libjpeg.so.8.2.2, symlink => libjpeg.so libjpeg.so.8
# Tar files in build step and untar in final image
RUN tar czf /testlib.tar.gz /usr/lib/libjpeg.so*

FROM base
LABEL name Fredrik Andersson

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE=1

# Copy neccesary files from builder image
COPY --from=builder /install /usr/local
COPY --from=builder /testlib.tar.gz /
RUN cd / && tar xzf testlib.tar.gz

RUN apk --no-cache add libpq

RUN mkdir /app
COPY ./app /app
WORKDIR /app

RUN adduser -D user

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web

USER user
