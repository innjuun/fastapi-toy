import redis
from rediscluster import RedisCluster

REDIS_ENDPOINT = "test.lkqmf4.ng.0001.apn2.cache.amazonaws.com"
REDIS_RO_ENDPOINT = "test-ro.lkqmf4.ng.0001.apn2.cache.amazonaws.com"
REDIS_CLUSTER_URL = "test-cluster.lkqmf4.clustercfg.apn2.cache.amazonaws.com"

redis_client = redis.Redis(host=REDIS_ENDPOINT, port=6379, db=0)

# startup_nodes = [
#     {"host": "test-cluster-0001-001.lkqmf4.0001.apn2.cache.amazonaws.com", "port": "6379"},
#     {"host": "test-cluster-0002-001.lkqmf4.0001.apn2.cache.amazonaws.com", "port": "6379"},
#     {"host": "test-cluster-0003-001.lkqmf4.0001.apn2.cache.amazonaws.com", "port": "6379"},
# ]

startup_nodes = [
    {"host": REDIS_CLUSTER_URL, "port": 6379}
]
redis_cluster_client = RedisCluster(
    startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True
)