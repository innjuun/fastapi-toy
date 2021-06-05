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
#
# def redis_instance(read_only: bool = False) -> StrictRedis:
#     return _get_redis_instance(read_only)
#
#
# def _get_redis_instance(read_only: bool = False) -> StrictRedis:
#     name = "readonly" if read_only else "default"
#     return caches[name].client.get_client()
#
#
# class PickleSerializer:
#     @staticmethod
#     def dumps(obj: Any) -> bytes:
#         return pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
#
#     @staticmethod
#     def loads(txt: bytes) -> Any:
#         return pickle.loads(txt)
#
#
# pickle_serializer = PickleSerializer()
#
#
# def cached(
#     *,
#     key_func: Callable[..., str],
#     expire_time: timedelta,
#     lock_timeout: float = 0,
#     serializer: SerializerProto = pickle_serializer,
#     redis_client_maker: Callable[[], StrictRedis] = _get_redis_instance,
# ):
#     """
#     파라미터 기반 캐시 데코레이터
#
#     :param key_func: 캐시 키 생성함수. 데코레이트 하는 함수를 호출할때 사용한 인자가 파리미터로 동일하게 전달됨.
#     :param expire_time: 캐시 보존 기간
#     :param lock_timeout: cache stampede 방지용 락/블럭 타임아웃 (초). 지정하지 않거나 0 지정하면 방지하지 않음.
#         데코레이트 되는 함수의 수행시간 고려해서 지정.
#     :param serializer: dumps / loads 동작 맞춤화용
#     :param redis_client_maker: 유닛 테스트용
#
#     - django_redis.client 인터페이스 직접 사용함. Django 버전올리면 하면 깨질 수 있음.
#     - 코드 변경시 `RUN_RISK_CACHE_TESTS=1 pytest targetyo/util/tests/test_cached.py` 로 테스트 해볼것
#     """
#
#     def decorator(f):
#         @wraps(f)
#         def wrapper(*args, **kwargs):
#             if not settings.PARAM_BASED_CACHE:
#                 return f(*args, **kwargs)
#             redis_client = redis_client_maker()
#
#             def invoke_wrapped():
#                 value = f(*args, **kwargs)
#                 raw = serializer.dumps(value)
#                 redis_client.setex(name=key, value=raw, time=expire_time)
#                 return value
#
#             key = key_func(*args, **kwargs)
#             raw_value = redis_client.get(key)
#             if raw_value is not None:
#                 # cache hit
#                 return serializer.loads(raw_value)
#
#             if not lock_timeout:
#                 # No cache stampede prevention
#                 return invoke_wrapped()
#
#             # https://en.wikipedia.org/wiki/Cache_stampede#Locking
#             lock = redis_client.lock(f"{key}:lock", timeout=lock_timeout, blocking_timeout=lock_timeout)
#             # NOTE: Do not use lock() as context manager.
#             #       Lock context manager try to release (redundant operation) even if it failed to acquire lock,
#             #       causing `redis.exceptions.LockError: Cannot release an unlocked lock`.
#             if lock.acquire():
#                 try:
#                     raw_value = redis_client.get(key)
#                     if raw_value is not None:
#                         return serializer.loads(raw_value)
#                     else:
#                         return invoke_wrapped()
#                 finally:
#                     try:
#                         # NOTE: 연산이 `lock_timeout` 보다 오래걸려서 락이 풀릴 수 있음. -> release 시도 -> LockError
#                         lock.release()
#                     except LockError:
#                         pass
#             else:
#                 return f(*args, **kwargs)
#
#         return wrapper
#
#     return decorator