import redis

import unittest
from unittest.mock import MagicMock
from redis_om import get_redis_connection

import os

class TestUserServices(unittest.TestCase):
  REDIS_URL = 'redis://localhost:6379'

  def setUp(self):
    pass
  
  async def test_redis_connection(self):
    redis_connection = redis.Redis.from_url(self.REDIS_URL)

    value = 'bar'
    await redis_connection.set('foo', value)
    result = await redis_connection.get('foo')
    redis_connection.close()

    self.assertEqual(result.decode(), value)