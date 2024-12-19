import time
import redis
import json
from dotmap import DotMap
import requests
from requests.exceptions import RequestException
from os import environ as env

class Connection:

    def __init__(self, api_key: str, api_url: str) -> None:
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.headers = {'Authorization': f'Token {self.api_key}', 'Content-Type': 'application/json'}

        # Redis configuration
        self.redis_host = env.get('REDIS_HOST', 'localhost')
        self.redis_port = int(env.get('REDIS_PORT', 6379))
        self.redis_db = int(env.get('REDIS_DB', 0))
        self.cache_ttl = int(env.get('CACHE_TTL', 86400))  # Default cache TTL to 1 day
        self.request_throttle_time = float(env.get('REQUEST_THROTTLE_TIME', 0.01))  # Default 10ms between requests

        # Initialize Redis connection
        self.redis = redis.StrictRedis(
            connection_pool=redis.ConnectionPool(
                host=self.redis_host, port=self.redis_port, db=self.redis_db, decode_responses=True))

    def link(self, pattern: str) -> str:
        """Generates a full API endpoint URL."""
        return f'{self.api_url}/{pattern}/'

    def is_request_throttled(self, user_id: int) -> bool:
        """
        Checks if the user has made a request recently within the throttle time.
        """
        cache_key = f'user_last_request:{user_id}'
        last_request_time = self.redis.get(cache_key)

        if last_request_time:
            last_request_time = float(last_request_time)
            current_time = time.time()
            if current_time - last_request_time < self.request_throttle_time:
                return True
        return False

    def update_last_request_time(self, user_id: int):
        """
        Updates the last request time for the user.
        """
        cache_key = f'user_last_request:{user_id}'
        self.redis.setex(cache_key, 1, time.time())  # Set TTL to 1 second

    @property
    def setting(self) -> DotMap:
        """
        Fetches settings from the API and caches them in Redis.
        """
        cache_key = 'ocrbot:setting_cache'
        cached_setting = self.redis.get(cache_key)
        if cached_setting:
            return DotMap(json.loads(cached_setting))

        # Fetch from API if not cached
        pattern = self.link('api/setting')
        try:
            res = requests.get(pattern, headers=self.headers)
            res.raise_for_status()  # Ensure a successful response
            setting_data = res.json()
            self.redis.setex(cache_key, self.cache_ttl, json.dumps(setting_data))
            return DotMap(setting_data)
        except RequestException as e:
            return DotMap({'error': str(e)})

    def user(self, chat_id: int, full_name=None, lang=None, is_admin=None, is_active=None, coin=None, last_coin_update=None) -> DotMap:
        """
        Fetches and updates user information from the API and caches it in Redis.
        Only chat_id is required; other fields are optional.
        """
        # Check rate limit
        if self.is_request_throttled(chat_id):
            return DotMap({'error': 'Request throttled. Please wait before making another request.'})

        pattern = self.link('api/user')
        data = {'chat_id': chat_id}
        
        # Add optional parameters if provided
        if full_name is not None:
            data['full_name'] = full_name
        if lang is not None:
            data['lang'] = lang
        if is_admin is not None:
            data['is_admin'] = is_admin
        if is_active is not None:
            data['is_active'] = is_active
        if coin is not None:
            data['coin'] = coin
        if last_coin_update is not None:
            data['last_coin_update'] = last_coin_update

        try:
            # Send user data to the API
            res = requests.post(pattern, headers=self.headers, json=data)
            res.raise_for_status()
            user_data = res.json()

            # Cache the response in Redis
            cache_key = f'user_cache_{chat_id}'
            self.redis.setex(cache_key, self.cache_ttl, json.dumps(user_data))

            # Update last request time
            self.update_last_request_time(chat_id)

            return DotMap(user_data)

        except RequestException as e:
            return DotMap({'error': str(e)})
        except redis.RedisError as e:
            return DotMap({'error': f'Redis connection error: {e}'})

    def create_payment(self, chat_id: int, plan: str) -> DotMap:
        """
        Creates a payment for the user based on the plan, and returns payment details.
        Uses GET method for payment creation.
        The URL is structured as: /api/payment/{chat_id}/{plan}/
        """
        # Check rate limit
        if self.is_request_throttled(chat_id):
            return DotMap({'error': 'Request throttled. Please wait before making another request.'})

        # Construct the URL for the payment API endpoint
        pattern = self.link(f'api/payment/{chat_id}/{plan}')  # Adjust URL format

        try:
            # Send GET request to create the payment
            res = requests.get(pattern, headers=self.headers)
            res.raise_for_status()
            payment_data = res.json()

            # Cache the response in Redis
            cache_key = f'payment_cache_{chat_id}_{payment_data["authority"]}'
            self.redis.setex(cache_key, self.cache_ttl, json.dumps(payment_data))

            # Update last request time
            self.update_last_request_time(chat_id)

            return DotMap(payment_data)

        except RequestException as e:
            return DotMap({'error': str(e)})
        except redis.RedisError as e:
            return DotMap({'error': f'Redis connection error: {e}'})

# Example usage
if __name__ == "__main__":
    connection = Connection(
        api_key="your_api_key",
        api_url="http://127.0.0.1:8000"
    )

    # Create a payment for the user
    payment_response = connection.create_payment(
        chat_id=1,  # Example chat_id
        plan="1"    # Example plan
    )
    print("Payment Response:", payment_response)

    # Fetch and update user information
    user_response = connection.user(
        chat_id=1,
        full_name='hi user',
        coin = 2345235 ,
        lang='fa'
    )
    print("User Response:", user_response)

    # Fetch application settings
    setting_response = connection.setting
    print("Setting Response:", setting_response)
