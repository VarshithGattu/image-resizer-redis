# config.py - Contains system-wide configuration settings

import os

# Redis configuration
# Use Render Redis if available, otherwise fallback to localhost for local testing
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# RQ Queue Name
QUEUE_NAME = 'image_tasks'

# Logging file
LOG_FILE = 'worker.log'

# Image resizing settings
RESIZE_WIDTH = 400
RESIZE_HEIGHT = 300