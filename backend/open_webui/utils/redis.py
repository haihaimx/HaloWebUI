import socketio
import redis
from redis import asyncio as aioredis
from redis.cluster import RedisCluster, ClusterNode
from urllib.parse import urlparse


def parse_redis_service_url(redis_url):
    parsed_url = urlparse(redis_url)
    if parsed_url.scheme != "redis":
        raise ValueError("Invalid Redis URL scheme. Must be 'redis'.")

    return {
        "username": parsed_url.username or None,
        "password": parsed_url.password or None,
        "service": parsed_url.hostname or "mymaster",
        "port": parsed_url.port or 6379,
        "db": int(parsed_url.path.lstrip("/") or 0),
    }


# Module-level connection pool cache: keyed by (redis_url, decode_responses)
_connection_pools: dict[tuple, redis.ConnectionPool] = {}

# Module-level cluster client cache: keyed by (redis_url, decode_responses)
_cluster_clients: dict[tuple, RedisCluster] = {}


def get_redis_connection(
    redis_url, redis_sentinels, decode_responses=True, cluster_mode=False
):
    if cluster_mode:
        # Redis Cluster mode: parse URL and create/reuse a cluster client
        cache_key = (redis_url, decode_responses)
        client = _cluster_clients.get(cache_key)
        if client is None:
            parsed = urlparse(redis_url)
            host = parsed.hostname or "localhost"
            port = parsed.port or 6379
            client = RedisCluster(
                startup_nodes=[ClusterNode(host, port)],
                username=parsed.username or None,
                password=parsed.password or None,
                decode_responses=decode_responses,
                skip_full_coverage_check=True,
            )
            _cluster_clients[cache_key] = client
        return client
    elif redis_sentinels:
        redis_config = parse_redis_service_url(redis_url)
        sentinel = redis.sentinel.Sentinel(
            redis_sentinels,
            port=redis_config["port"],
            db=redis_config["db"],
            username=redis_config["username"],
            password=redis_config["password"],
            decode_responses=decode_responses,
        )

        # Get a master connection from Sentinel
        return sentinel.master_for(redis_config["service"])
    else:
        # Reuse a shared ConnectionPool for the same (url, decode_responses) pair
        pool_key = (redis_url, decode_responses)
        pool = _connection_pools.get(pool_key)
        if pool is None:
            pool = redis.ConnectionPool.from_url(
                redis_url, decode_responses=decode_responses
            )
            _connection_pools[pool_key] = pool
        return redis.Redis(connection_pool=pool)


def get_sentinels_from_env(sentinel_hosts_env, sentinel_port_env):
    if sentinel_hosts_env:
        sentinel_hosts = sentinel_hosts_env.split(",")
        sentinel_port = int(sentinel_port_env)
        return [(host, sentinel_port) for host in sentinel_hosts]
    return []


def get_sentinel_url_from_env(redis_url, sentinel_hosts_env, sentinel_port_env):
    redis_config = parse_redis_service_url(redis_url)
    username = redis_config["username"] or ""
    password = redis_config["password"] or ""
    auth_part = ""
    if username or password:
        auth_part = f"{username}:{password}@"
    hosts_part = ",".join(
        f"{host}:{sentinel_port_env}" for host in sentinel_hosts_env.split(",")
    )
    return f"redis+sentinel://{auth_part}{hosts_part}/{redis_config['db']}/{redis_config['service']}"
