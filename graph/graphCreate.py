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
@describe: RedisGraph建表
"""
import json

from redisgraph import Graph

from config.redisContent import RedisContent


class GraphRedisCreate:
    def __init__(self, graph_name='COM'):
        """
        :param graph_name: 所创建的图表名称
        """
        self._redis_content = RedisContent().get_content
        self._redis_graph = Graph(graph_name, self._redis_content)
        self.index = 0

    def create_node(self, args):
        """
        创建图节点
        eg: CREATE (c"简称":company"公司节点名称"),
        (p"简称":position"职位节点名称"),
        (c)-[:have]->(p),    # 公司与职位建立对应关系，公司拥有某职位，相当于MySQL表连接
        (p)-[:belong]->(c)   # 公司与职位建立对应关系，该职位属于某公司，相当于MySQL表连接
        :param args: 节点参数
        :return:
        """
        companyName, positionName, source, workAddress, companyAddress, workBackground, workBackgroundStandard = args
        query_sql = '''CREATE
            (c:company {companyName:"%s", companyAddress: "%s", source: "%s"}),
            (p:position {positionName :"%s", workAddress: "%s", workBackground: "%s", workBackgroundStandard: "%s"}),
            (c)-[:have]->(p),
            (p)-[:belong]->(c)
        ''' % (companyName, companyAddress, source, positionName, workAddress, workBackground, workBackgroundStandard)
        print(query_sql)
        self.index += 1
        # print(dict_position, dict_position)
        print('插入第：', self.index)
        # 创建图节点
        self._redis_graph.query(query_sql)

    def read_json_file(self):
        f = open('../data/recruitMsg.json', 'r', encoding='utf-8')
        recruit = json.load(f)
        for data in recruit:
            companyName = data['companyName']  # 公司名称
            positionName = data['positionName']  # 职位名称
            source = data['source']  # 招聘来源
            workAddress = data['workAddress']  # 工作地址
            companyAddress = data['companyAddress']  # 公司地址
            workBackground = data['workBackground']  # 工作年限
            workBackgroundStandard = data['workBackgroundStandard']  # 工作经验
            msg = [companyName, positionName, source, workAddress, companyAddress, workBackground,
                   workBackgroundStandard]

            self.create_node(msg)  # 创建图节点


if __name__ == '__main__':
    g = GraphRedisCreate()
    g.read_json_file()
