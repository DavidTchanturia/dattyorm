from redis_orm.redis_orm import RedisORM

redis_orm = RedisORM()

redis_orm.insert_into_redis("user:1", {'name':'John', 'age':22})
redis_orm.insert_into_redis("user:2", {'name':'John', 'age':23})
redis_orm.insert_into_redis("user:3", {'name':'John', 'age':23})
redis_orm.insert_into_redis("user:4", {'name':'John', 'age':223})

users = redis_orm.select_all("user*")
redis_orm.export_all_to_json()