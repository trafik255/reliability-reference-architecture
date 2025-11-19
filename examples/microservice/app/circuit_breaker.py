# app/circuit_breaker.py

import time
from enum import Enum


class State(Enum):
    CLOSED = "closed"          # normal
    OPEN = "open"              # failing fast
    HALF_OPEN = "half_open"    # test mode


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 5,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = None

    def _trip(self):
        self.state = State.OPEN
        self.last_failure_time = time.time()

    def _attempt_reset(self):
        if time.time() - self.last_failure_time >= self.recovery_timeout:
            self.state = State.HALF_OPEN

    def call(self, func):
        if self.state == State.OPEN:
            self._attempt_reset()

        if self.state == State.OPEN:
            raise Exception("CircuitBreaker: OPEN (failing fast)")

        try:
            result = func()

            # success in HALF_OPEN → close the circuit
            if self.state == State.HALF_OPEN:
                self.state = State.CLOSED
                self.failure_count = 0

            return result

        except Exception:
            self.failure_count += 1

            if self.failure_count >= self.failure_threshold:
                self._trip()

            raise
