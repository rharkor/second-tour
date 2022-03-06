#!/bin/bash
service nginx start
sh && cd /app/website/secondtour_website && uwsgi /app/website/secondtour_website/website.ini
# ls /app/website/secondtour_website