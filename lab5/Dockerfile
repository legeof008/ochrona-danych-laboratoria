FROM nginx
RUN  rm /usr/share/nginx/html/*
COPY load /usr/share/nginx/html
RUN  mkdir -p /etc/apache2
RUN  rm /etc/nginx/nginx.conf
COPY .htpasswd /etc/apache2
COPY nginx.conf /etc/nginx
