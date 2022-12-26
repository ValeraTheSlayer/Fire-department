FROM nginx:1.19.0-alpine

RUN apk add --no-cache tzdata
ENV TZ Asia/Almaty

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d
