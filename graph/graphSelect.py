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
@describe: 
"""
import sys
import os

from redisgraph import Graph
from config.redisContent import RedisContent

sys.path.append(os.path.dirname(os.getcwd()))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/' + '..'))
'''// 1 统计职位名称相同的 count
MATCH (NodeName_one:company)-[:have]->(NodeName_two:position) 
WHERE NodeName_two.positionEducation="本科及以上"
RETURN NodeName_two.positionName,COUNT(NodeName_two.positionName)
// 2 MAX, MIN , AVG
MATCH (NodeName_one:company)-[:have]->(NodeName_two:position) 
WHERE NodeName_two.positionEducation="本科及以上"
RETURN NodeName_two.positionEducation, MAX(NodeName_two.positionPriceAvg) 
// 3 MAX, MIN , AVG 复杂查询
MATCH (NodeName_one:company)-[:have]->(NodeName_two:position) 
WHERE NodeName_two.positionName="本科及以上"
RETURN NodeName_two.positionEducation,NodeName_two.positionName,MAX(NodeName_two.positionPriceAvg),COUNT(NodeName_two.positionName)
'''


class GraphSelect:
    def __init__(self, graph_name='COM'):
        """
        :param graph_name: 所创建的图表名称
        """
        self._redis_content = RedisContent().get_content
        self._redis_graph = Graph(graph_name, self._redis_content)
        self.index = 0

    def get_graph_msg(self, query_sql):
        back_msg = self._redis_graph.query(query_sql)
        print("结果:", back_msg.pretty_print())
        return back_msg.result_set[1:]

    def select_all(self):
        """
            全表查询
        :return:
        """
        query_sql = '''
            MATCH (c:company)-[:have]->(p:position)
            RETURN c,p
        '''
        self.get_graph_msg(query_sql)

    def select_where(self):
        """
            查询招聘信息来源于58同城的
        :return:
        """
        query_sql = '''
            MATCH (c:company)-[:have]->(p:position)
            WHERE c.source="58同城招聘"
            RETURN c,p
        '''
        self.get_graph_msg(query_sql)

    def select_work(self):
        """
            查询工作地点在北京的公司名称，职位名称
        :return:
        """
        query_sql = '''
            MATCH (c:company)-[:have]->(p:position)
            WHERE p.workAddress="北京"
            RETURN c.companyName,p.positionName
        '''
        self.get_graph_msg(query_sql)


if __name__ == '__main__':
    g = GraphSelect()
    g.select_all()
