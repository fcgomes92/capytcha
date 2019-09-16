FROM python:alpine

WORKDIR /app

COPY requirements.txt /app/
COPY ./ /app

RUN apk add alpine-sdk make gcc g++ 
RUN make docker_build

RUN pip3 install -r requirements.txt
RUN pip3 install dist/capytcha-*.whl

RUN rm -R capytcha

EXPOSE 8080

CMD ["capytcha-serve"]