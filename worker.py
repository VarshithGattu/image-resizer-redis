import redis
from rq import Connection, SimpleWorker

# Windows workaround for RQ timeout system
class FakeDeathPenalty:
    def __init__(self, *args, **kwargs): pass
    def __enter__(self): return self
    def __exit__(self, *args, **kwargs): pass

class WindowsWorker(SimpleWorker):
    death_penalty_class = FakeDeathPenalty
    def setup_death_penalty(self): pass

redis_conn = redis.from_url("redis://127.0.0.1:6379/0")

if __name__ == "__main__":
    with Connection(redis_conn):
        worker = WindowsWorker(["image_tasks"])
        print("--- Windows Worker (Emergency Mode) starting ---")
        worker.work()