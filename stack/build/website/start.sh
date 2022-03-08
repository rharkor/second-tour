#!/bin/bash
service nginx start
sh && cd /app/website/secondtour_website/ && uwsgi website.ini
