#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@software: PyCharm 
@file: alipayTestOne.py 
@time: 
@describe: reids连接对象
"""
from config.readSetting import ReadSetting
import redis

class RedisContent:
    def __init__(self, content_name='redis_content_graph'):
        """
        创建redis连接池
        :param content_name: setting.yaml配置连接名
        """
        self._setting = ReadSetting().read_yaml[content_name]

        self._pool = redis.ConnectionPool(host=self._setting['REDIS_HOST'], port=self._setting['REDIS_PORT'],
                                         db=self._setting['REDIS_DB'], password=self._setting['REDIS_PASSWD'])
    @property
    def get_content(self):
        """
        返回Redis连接对象
        :return:
        """
        return redis.Redis(connection_pool=self._pool)