#!bin/bash

gunicorn -D -w 3 -b 127.0.0.1:8000 app:app
