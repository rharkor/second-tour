ARG VERSION

# Dev image
FROM ubuntu:latest




# Update & install nginx & python
RUN apt-get update && apt-get install -y nginx \
    && apt-get install nano \
    && apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools \
    && rm /etc/nginx/sites-enabled/default
RUN mkdir -p /app/website/secondtour_website 

COPY ./website/secondtour_website/requirements.txt /app/website/secondtour_website/requirements.txt
COPY ./build/website/start.sh /app/scripts/start.sh

RUN pip install -r /app/website/secondtour_website/requirements.txt

# Copy nginx config
COPY ./build/website/uwsgi.conf /etc/nginx/uwsgi_params
COPY ./build/website/default.conf /etc/nginx/sites-enabled/secondtour_website


# CMD ["nginx", "-g", "daemon", "off;"]
# CMD ["uwsgi", "/app/website/secondtour_website/website.ini"]
CMD ["bash", "/app/scripts/start.sh"]

EXPOSE 80


