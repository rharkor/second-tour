#!/bin/bash
service nginx start
cd /app/api/secondtour_api && uvicorn main:app --host 0.0.0.0 --port 443 &
cd /app/website/secondtour_website && uwsgi /app/website/secondtour_website/website.ini
