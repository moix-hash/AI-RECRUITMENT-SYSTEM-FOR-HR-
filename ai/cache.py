from __future__ import annotations

import functools
from typing import Any

from config.settings import ENABLE_CACHE


def cached(func):
    if not ENABLE_CACHE:
        return func

    cache_store: dict[str, Any] = {}

    def wrapper(*args, **kwargs):
        key = f"{func.__name__}:{args}:{kwargs}"
        if key in cache_store:
            return cache_store[key]
        result = func(*args, **kwargs)
        cache_store[key] = result
        return result

    return wrapper
