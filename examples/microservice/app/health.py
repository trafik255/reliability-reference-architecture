# app/health.py

def get_liveness():
    return {"status": "live"}


def get_readiness():
    # TODO: plug in real dependency checks (DB, queues, etc.)
    return {"status": "ready"}
