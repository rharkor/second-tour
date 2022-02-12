#!/bin/bash
service nginx start
cd /app/website/secondtour_website && uwsgi /app/website/secondtour_website/website.ini
