FROM python:alpine

EXPOSE 8080

WORKDIR /app

COPY ./ /app

RUN apk --no-cache add alpine-sdk \
    make \
    gcc \
    g++ \
    make \
    python \
    python3 \
    build-base \
    python-dev \
    python3-dev \
    # Pillow dependencies
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    tk-dev \
    tcl-dev \
    harfbuzz-dev \
    fribidi-dev

ENTRYPOINT [ "make" ]

CMD ["run"]