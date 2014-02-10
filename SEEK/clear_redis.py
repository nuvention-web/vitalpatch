from redis import Redis
import os
redis_url = os.getenv('REDISTOGO_URL')
redis_instance = Redis.from_url(redis_url)
redis_instance.hdel("user1", "ip", "latitude", "longitude", "isHere")
redis_instance.hdel("user2", "ip", "latitude", "longitude", "isHere")