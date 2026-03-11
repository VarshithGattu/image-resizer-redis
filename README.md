# Async Image Resizer

A web application that resizes images asynchronously using:

- Flask (Web Framework)
- Redis (Message Broker)
- RQ (Background Worker Queue)
- Pillow (Image Processing)

## Features
- Upload images
- Resize images in background
- Retry mechanism for failed jobs
- Worker-based architecture

## Tech Stack
Python, Flask, Redis, RQ, Pillow

## How to Run

1. Start Redis
redis-server

2. Run worker
python worker.py

3. Start Flask
python app.py
