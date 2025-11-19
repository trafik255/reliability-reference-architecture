# app/reliability.py

import random
import time
from .circuit_breaker import CircuitBreaker, State


breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=5,
)


class DownstreamError(Exception):
    pass


def _flaky_downstream_call():
    """
    Simulates a 50% failure rate.
    """
    if random.random() < 0.5:
        raise DownstreamError("Downstream service failed")
    return "success"


def flaky_with_retries(max_retries=3, base_delay_seconds=0.1):
    """
    Retry logic + Backoff + Circuit Breaker wrapping.
    """

    def attempt():
        return _flaky_downstream_call()

    attempt_number = 0

    while True:
        try:
            # circuit breaker wraps the call
            return breaker.call(attempt)

        except Exception as exc:
            attempt_number += 1

            if attempt_number > max_retries:
                raise exc

            # exponential backoff
            sleep_for = base_delay_seconds * (2 ** (attempt_number - 1))
            time.sleep(sleep_for)
