import json
import os
from dataclasses import dataclass
from typing import Any, Optional

import redis


@dataclass(frozen=True)
class RedisSettings:
    url: str
    cache_ttl_seconds: int
    idempotency_ttl_seconds: int
    rate_limit_per_sec: int


def load_redis_settings() -> RedisSettings:
    return RedisSettings(
        url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "2")),
        idempotency_ttl_seconds=int(os.getenv("IDEMPOTENCY_TTL_SECONDS", "300")),
        rate_limit_per_sec=int(os.getenv("RATE_LIMIT_PER_SEC", "20")),
    )


class RedisClient:
    def __init__(self, settings: RedisSettings):
        self._settings = settings
        self._r = redis.Redis.from_url(settings.url, decode_responses=True)

    def ping(self) -> bool:
        return self._r.ping()

    # ---------- cache ----------
    def cache_get_json(self, key: str) -> Optional[dict[str, Any]]:
        raw = self._r.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def cache_set_json(self, key: str, value: dict[str, Any], ttl_seconds: Optional[int] = None) -> None:
        ttl = ttl_seconds if ttl_seconds is not None else self._settings.cache_ttl_seconds
        self._r.set(key, json.dumps(value), ex=ttl)

    def cache_del(self, key: str) -> None:
        self._r.delete(key)

    # ---------- idempotency ----------
    def idem_get(self, key: str) -> Optional[dict[str, Any]]:
        raw = self._r.get(key)
        if raw is None:
            return None
        return json.loads(raw)

    def idem_set(self, key: str, response_payload: dict[str, Any]) -> None:
        self._r.set(key, json.dumps(response_payload), ex=self._settings.idempotency_ttl_seconds)

    # ---------- rate limit ----------
    def rate_limit_hit(self, key: str, limit_per_sec: int) -> tuple[int, bool]:
        """
        Returns (current_count, allowed)
        """
        count = self._r.incr(key)
        if count == 1:
            self._r.expire(key, 1)
        return count, (count <= limit_per_sec)
