FROM nginx:1.18-alpine

RUN mkdir -p /var/www/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d