#!/usr/bin/env python  
# encoding: utf-8  
""" 
@version: v1.0 
@author: W_H_J 
@license: Apache Licence  
@contact: 415900617@qq.com 
@site:  
@software: PyCharm 
@file: readSetting.py
@time: 2018/4/28 10:14 
@describe: 读取配置文件
"""
import yaml


class ReadSetting:
    def __init__(self):
        self.filename = '../setting.yaml'

    @property
    def read_yaml(self):
        """
        读取配置文件
        :return:
        """
        try:
            with open(self.filename) as f:
                y = yaml.load(f)
            return y
        except Exception as e:
            raise Exception('No content name in setting!',e)