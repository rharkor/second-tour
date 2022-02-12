#!/bin/bash
cd /app/api/secondtour_api && uvicorn main:app --host 0.0.0.0 --port 443 