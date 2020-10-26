FROM tiangolo/uwsgi-nginx-flask:python3.6

COPY ./app /app

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

ENV NGINX_MAX_UPLOAD 10m

EXPOSE 80
