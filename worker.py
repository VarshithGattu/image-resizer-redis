import redis
from rq import SimpleWorker, Queue
from redis import Redis
import os

# Get Redis URL from environment variable (important for Render)
redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")

# Connect to Redis
conn = Redis.from_url(redis_url)

# Queue name (must match config.py)
queue = Queue("image_tasks", connection=conn)

# Windows-safe fake death penalty
class FakeDeathPenalty:
    def __init__(self, *args, **kwargs): 
        pass
    def __enter__(self): 
        return self
    def __exit__(self, *args): 
        pass

class WindowsWorker(SimpleWorker):
    death_penalty_class = FakeDeathPenalty
    def setup_death_penalty(self): 
        pass


if __name__ == "__main__":
    worker = WindowsWorker([queue], connection=conn)
    print("--- Worker started ---")
    worker.work()