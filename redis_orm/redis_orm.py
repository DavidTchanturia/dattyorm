import redis
import json
import pandas as pd

class RedisORM:
    def __init__(self, host='localhost', port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def _serialize_data(self, data):
        return json.dumps(data)

    def _deserialize_data(self, serialized_data):
        if serialized_data:
            return json.loads(serialized_data)
        return None

    def insert_into_redis(self, key, data):
        serialized_data = self._serialize_data(data)
        self.redis_client.set(key, serialized_data)

    def select_from_redis(self, key):
        serialized_data = self.redis_client.get(key)
        return self._deserialize_data(serialized_data)

    def select_all(self, pattern='*'):
        keys = self.redis_client.keys(pattern)
        data = {}
        for key in keys:
            decoded_key = key.decode('utf-8')
            data[decoded_key] = self.select_from_redis(decoded_key)
        return data

    def update_data(self, key, new_data):
        current = self.select_from_redis(key)
        if current:
            current.update(new_data)
            self.insert_into_redis(key, current)
        else:
            print("Key not found")

    def delete(self, key):
        self.redis_client.delete(key)


    def export_all_to_csv(self, pattern='*', file_path="redis_data.csv"):
        data = self.select_all(pattern)
        df = pd.DataFrame.from_dict(data, orient='index')
        df.to_csv(file_path, index_label='Key')
        print("Data inserted into CSV successfully.")

    def export_all_to_json(self, pattern='*', file_path="redis_data.json"):
        data = self.select_all(pattern)
        df = pd.DataFrame.from_dict(data, orient='index')
        df.to_json(file_path, orient='index', indent=4)
        print(f"Data exported to {file_path} successfully.")

redis_orm = RedisORM()
redis_orm.insert_into_redis("user:1", {'name':'John', 'age':22})
redis_orm.insert_into_redis("user:2", {'name':'John', 'age':23})
redis_orm.insert_into_redis("user:3", {'name':'John', 'age':23})
redis_orm.insert_into_redis("user:4", {'name':'John', 'age':223})

users = redis_orm.select_all("user*")
redis_orm.export_all_to_json()