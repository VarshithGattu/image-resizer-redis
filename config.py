# config.py - Contains system-wide configuration settings

# Redis configuration (default for local installation/WSL)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'

# RQ Queue Name
QUEUE_NAME = 'image_tasks'

# Logging file
LOG_FILE = 'worker.log'

# Image resizing settings
RESIZE_WIDTH = 400
RESIZE_HEIGHT = 300