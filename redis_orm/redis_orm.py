import redis
import json
import pandas as pd
from utils.orm_logger import setup_logging
import logging


setup_logging()
logger = logging.getLogger(__name__)


class RedisORM:
    def __init__(self, host='localhost', port=6379):
        self.redis_client = redis.Redis(host=host, port=port)

    def insert_into_redis(self, key, data):
        """key could be automatically generated, but then user would not be able to find them,
        user needs to specify the key and then the data

        for instance
        person:1 -> {"name": "john", "age": 32}"""
        serialized_data = self._serialize_data(data)
        self.redis_client.set(key, serialized_data)

    def select_from_redis(self, key):
        """select specific values based on the key"""
        serialized_data = self.redis_client.get(key)
        return self._deserialize_data(serialized_data)

    def select_all(self, pattern='*'):
        """select all
        TO KEEP IN MIND !!!!!!!
        since redis can have other data as well
        you will have to verify the patter
        for instance to select all data with key person
        pattern=person*
        """
        try:
            keys = self.redis_client.keys(pattern)
            data = {}
            for key in keys:
                decoded_key = key.decode('utf-8')
                data[decoded_key] = self.select_from_redis(decoded_key)
            return data
        except json.decoder.JSONDecodeError: # happens when trying to select all the keys but their patter does not match
            logger.error("patterns does not match, please specify")

    def update_data(self, key, new_data):
        current = self.select_from_redis(key)
        if current:
            current.update(new_data)
            self.insert_into_redis(key, current)
        else:
            logger.info(f"No data found for key {key}")

    def delete(self, key):
        current = self.select_from_redis(key)
        if current:
            self.redis_client.delete(key)
        else:
            logger.info(f"No data found for key {key}")

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


    def _serialize_data(self, data):
        """turn class object into json"""
        return json.dumps(data)

    def _deserialize_data(self, serialized_data):
        """get class object from serialized_dat"""
        if serialized_data:
            return json.loads(serialized_data)
        return None