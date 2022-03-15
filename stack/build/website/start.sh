#!/bin/sh
sleep 5 && echo "Restart nginx" && service nginx start &
cd /app/website/secondtour_website/ && uwsgi website.ini