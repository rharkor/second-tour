ARG VERSION

# Dev image
FROM ubuntu:latest

# Update & install python
RUN apt-get update
RUN apt-get install nano
RUN apt install -y python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools

# Install the api requirements
COPY ./api/secondtour_api/requirements.txt /app/api/secondtour_api/requirements.txt
RUN pip install -r /app/api/secondtour_api/requirements.txt


# RUN systemctl start secondtour_website
# RUN systemctl enable secondtour_website

# Copy the startup script
COPY ./build/api/start.sh /app/scripts/start.sh

# Prod image
EXPOSE 443

CMD ["/app/scripts/start.sh"]
