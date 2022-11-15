FROM tiangolo/uwsgi-nginx-flask
# NGIX CONFIG
RUN  rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx
# PYTHON CONFIG
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools
RUN pip3 install bcrypt
# COPY PYTHON APP
RUN mkdir -p /opt/custom/flaskapp
COPY app /opt/custom/flaskapp

# CONFIG UWSGI
ENV UWSGI_INI /opt/custom/flaskapp/uwsgi.ini
WORKDIR /opt/custom/flaskapp

EXPOSE 80