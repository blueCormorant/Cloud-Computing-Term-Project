#!/bin/bash
celery -A celery_worker worker -E --loglevel=INFO --logfile worker1.log -n worker1 -P eventlet -c 5 &
celery -A celery_worker worker -E --loglevel=INFO --logfile worker2.log -n worker2 -P eventlet -c 5 &
celery -A celery_worker worker -E --loglevel=INFO --logfile worker3.log -n worker3 -P eventlet -c 5 &
