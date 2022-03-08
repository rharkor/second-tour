ARG VERSION

# Dev image
FROM ubuntu:latest

# Update & install nginx & python
RUN apt-get update && apt-get install -y nginx
RUN apt-get install nano
RUN apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

# Copy nginx config
COPY ./build/website/uwsgi.conf /etc/nginx/uwsgi_params
COPY ./build/website/default.conf /etc/nginx/sites-enabled/secondtour_website
# Remove the default file
RUN rm /etc/nginx/sites-enabled/default


# Create de app directory
RUN mkdir -p /app/website/secondtour_website

# Install the requirements
COPY ./website/secondtour_website/requirements.txt /app/website/secondtour_website/requirements.txt
RUN pip install -r /app/website/secondtour_website/requirements.txt


# RUN systemctl start secondtour_website
# RUN systemctl enable secondtour_website


# Prod image
EXPOSE 80

CMD ["uwsgi","/app/website/secondtour_website/website.ini"]
