import logging

# Broker settings
broker_url = 'redis://localhost:6379/0'

# Result backend settings
result_backend = 'redis://localhost:6379/1'

task_default_queue = 'low_priority'
task_routes = {
    'tasks.translate_file': {'queue': 'low_priority'},
}

# Task settings
accept_content = ['json']
task_serializer = 'json'
result_serializer = 'json'
timezone = 'UTC'

# Worker settings
worker_concurrency = 8
worker_prefetch_multiplier = 4

# Set the log level to INFO
CELERYD_LOG_LEVEL = logging.INFO

# Configure the logging format
worker_log_format = '%(asctime)s [%(levelname)s] %(message)s'
worker_task_log_format = '%(asctime)s [%(levelname)s] [%(task_name)s(%(task_id)s)] %(message)s'

# Configure the logging handlers
CELERYD_LOG_FILE = 'worker.log'
CELERYD_LOG_REDIRECT = True
