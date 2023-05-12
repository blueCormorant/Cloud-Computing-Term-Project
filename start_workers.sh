#!/bin/bash
celery -A celery_worker worker -E --loglevel=INFO -n worker1 -P eventlet -c 1 &
celery -A celery_worker worker -E --loglevel=INFO -n worker2 -P eventlet -c 1 &
celery -A celery_worker worker -E --loglevel=INFO -n worker3 -P eventlet -c 1 &
