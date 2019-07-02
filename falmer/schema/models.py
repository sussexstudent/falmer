import hashlib

from django.db import models
from django.core.cache import cache


def hash_query(query: str) -> str:
    return hashlib.sha256(query.encode('utf-8')).hexdigest()


def cache_key(query_hash: str) -> str:
    return f'pq:{query_hash}'


class PersistedQuery(models.Model):
    sha256_hash = models.CharField(max_length=256, blank=False, null=False, db_index=True, unique=True)
    query = models.TextField(blank=False, null=False, unique=True)

    def cache(self):
        cache.set(cache_key(self.sha256_hash), self.query, 2 * 7 * 24 * 60 * 60)

    @staticmethod
    def get_from_hash(client_hash: str):
        cached = cache.get(cache_key(client_hash), None)

        if cached is not None:
            return cached

        try:
            pq = PersistedQuery.objects.get(sha256_hash=client_hash).query
            pq.cache()
            return pq.query
        except PersistedQuery.DoesNotExist:
            return None

    @staticmethod
    def create_from_query(query: str, client_hash: str) -> bool:
        server_hash = hash_query(query)

        if server_hash != client_hash:
            return False

        pq = PersistedQuery.objects.create(
            sha256_hash=server_hash,
            query=query,
        )

        pq.cache()

        return True

