#!/bin/sh
service nginx start && sleep 10 && cd /app/website/secondtour_website && uwsgi /app/website/secondtour_website/website.ini