"""Simple caching utilities for performance optimization"""
from typing import Any, Dict, Optional, Callable
from datetime import datetime, timedelta
from functools import wraps
import threading


class SimpleCache:
    """Thread-safe in-memory cache with TTL support

    This cache is designed for caching expensive operations like
    file reads, API calls, or computation results.

    Examples:
        >>> cache = SimpleCache(ttl_seconds=300)  # 5 minute TTL
        >>> cache.set("key", "value")
        >>> cache.get("key")
        'value'
        >>> cache.clear()
    """

    def __init__(self, ttl_seconds: int = 300):
        """Initialize cache

        Args:
            ttl_seconds: Time to live for cache entries in seconds (default: 300)
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.ttl_seconds = ttl_seconds

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache

        Args:
            key: Cache key

        Returns:
            Cached value or None if not found or expired
        """
        with self._lock:
            if key not in self._cache:
                return None

            entry = self._cache[key]
            expiry = entry.get('expiry')

            # Check if expired
            if expiry and datetime.now() > expiry:
                del self._cache[key]
                return None

            return entry.get('value')

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set value in cache

        Args:
            key: Cache key
            value: Value to cache
            ttl_seconds: Optional TTL override for this entry
        """
        ttl = ttl_seconds if ttl_seconds is not None else self.ttl_seconds
        expiry = datetime.now() + timedelta(seconds=ttl) if ttl > 0 else None

        with self._lock:
            self._cache[key] = {
                'value': value,
                'expiry': expiry,
                'created': datetime.now()
            }

    def delete(self, key: str) -> None:
        """Delete entry from cache

        Args:
            key: Cache key to delete
        """
        with self._lock:
            if key in self._cache:
                del self._cache[key]

    def clear(self) -> None:
        """Clear all cache entries"""
        with self._lock:
            self._cache.clear()

    def cleanup_expired(self) -> int:
        """Remove all expired entries

        Returns:
            Number of entries removed
        """
        removed = 0
        now = datetime.now()

        with self._lock:
            keys_to_remove = [
                key for key, entry in self._cache.items()
                if entry.get('expiry') and now > entry['expiry']
            ]

            for key in keys_to_remove:
                del self._cache[key]
                removed += 1

        return removed

    def size(self) -> int:
        """Get current cache size

        Returns:
            Number of entries in cache
        """
        with self._lock:
            return len(self._cache)


def cached(cache_instance: SimpleCache, key_func: Optional[Callable] = None, ttl: Optional[int] = None):
    """Decorator for caching function results

    Args:
        cache_instance: Cache instance to use
        key_func: Optional function to generate cache key from args/kwargs
        ttl: Optional TTL override

    Examples:
        >>> cache = SimpleCache()
        >>> @cached(cache)
        ... def expensive_function(x):
        ...     return x * 2
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default: use function name + stringified args
                cache_key = f"{func.__name__}:{str(args)}:{str(kwargs)}"

            # Try to get from cache
            result = cache_instance.get(cache_key)
            if result is not None:
                return result

            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_instance.set(cache_key, result, ttl_seconds=ttl)
            return result

        return wrapper
    return decorator
