# RedisGraph探索结果[官方文档](https://oss.redislabs.com/redisgraph/)

---

基于Github上2018年6月24日更新版本

---

[TOC]

## 1.RedisGraph是什么?

###关于Redis 4.0 Modules特性

在Redis4.0版本中,引入了Redis Modules的概念.Redis4.0开放了Redis Modules API通过这个API,开发者可以自定义Redis的命令以及自定义实现功能,提供了使得可以通过外部模块对Redis进行功能拓展.Redis的模块采用动态链接库的形式,在启动的时候加载,也可以在运行时加载.

RedisGraph正是由[swilly22](https://github.com/swilly22)团队基于这种特性开源实现的一种**支持Cyper语言查询的、高性能、内存图数据库**.

## 2.RedisGraph能做什么?

### 功能介绍

Redisgraph基于Redis Modules API拓展Redis并提供了一些新的命令和功能.主要提供的图数据的**构建**、**查询**、**过滤**、**排序**、**聚合**等操作.Redisgraph使用C语言编写,数据底层通过实现了一种称为`Hexastore`的三元组存储结构,为图搜索操作提供了高效的支持,并以数据表形式给出查询结果集.

一个`Hexastore`结构由一组的三元组列表构成,三元组的结构:

```json
主语(Subject) -[谓语(Predicate)] -> 目标(Object)
```



`Hexastore`在存储三元组时会将SPO的进行排列组合为六种三元组进行存储到内存中,以提供高效快速的搜索.

###优势

1. 创建速度快.RedisGraph建立一条关系用时只需0.1ms.
2. 查询速度快,以Hexastore作为存储结构且基于内存操作,查询效率较其他图数据库有优势.
3. 构建方便,基于Redis4.0完成模块化功能.
4. 操作简单,基于Redis自定义命令使用Cypher语句进行关系图操作.

###局限

1. 现阶段不支持数据持久化.对于基于Redis Module API构建的新的数据结构,Redis自身的持久化功能并不能生效.
3. 对于`,`   `， `   `"`  等字符的存储不支持.

## 3.如何使用Redisgraph?

### 构建RedisGraph模块

1. 克隆RedisGraph模块: git clone https://github.com/RedisLabsModules/redis-graph.git
2. 安装build-essential和cmake包: apt-get install build-essential cmake
3. 在克隆的RedisGraph目录下执行`make`,然后在`src` 目录下找到编译的模块库`redisgraph.so`

### 加载RedisGraph(Redis4.0及以上版本)

两种加载方式:

1. 在`redis.conf` 文件中添加`loadmodule /path/module/src/redisgraph.so`,启动Redis.
2. 使用`redis-server --loadmodule /path/module/src/redisgraph.so` 命令启动Redis.

启动redis后,若加载成功RedisGraph模块,则会显示如下日志:


### 使用RedisGraph

#### 自定义命令:GRAPH.QUERY

```sql
GRAPH.QUERY key ...options...
```

**功能**:针对指定的图执行给定的查询

**参数**:key-- 图名称、options--查询语句

**返回值**: 数据表结果集

例: 根据节点和关系查询数据集

```sql
GRAPH.QUERY recruitMsg "match (com:Company)-[:have]->(pos:Position)"
```



#### QUERY关键字

- MATCH  查询
- WHERE 条件过滤
- RETURN 返回结果
- ORDER BY 排序
- LIMIT 限制查询返回记录数
- CREATE 创建新的节点和关系
- DELETE 删除节点和关系
- SET 修改节点和关系的属性值

#### 聚合函数

- sum 求和
- avg  平均数
- min 最小值
- max 最大值
- count 计数





## 4.基于招聘数据的RedisGraph应用

### 1.创建关系图

```sql
GRAPH.QUERY COM 'CREATE (com:company{companyName:"",type:"",...}),
						 (pos:position{positionName:"",source:"",...}),
						 (com)-[:have]->(pos),
						 (pos)-[:belong]->(com)'
```


### 2.查询

查询'公司拥有职位'关系图中的职位名称、职位最低薪资、职位最高薪资.

```sql
GRAPH.QUERY COM 'MATCH (com:company)-[:have]->(pos:position)RETURN pos.positionName,pos.positionPriceLower,pos.positionPriceTop'
```


## 5.总结

RedisGraph现阶段还处于开发阶段,还有很多功能未来得及实现且社区还不够完善，但基本增删改查以满足传统业务需求。

总体来说RedisGraph提供了一些基础的图数据库的基本操作,适用于构建简单的关系图.开发者能够通过提供的API构建、查询关系图,也得益于其基于内存存储和Hexastore数据结构的特性,使得查询效率较其他图数据库有明显的优势.但还存在着如上文提到的很多的局限性，但是redisgraph的出现解决了Redis传统的五种数据结构，极大扩展了Redis的热数据存储功能，通过它我们可以将MySQL的热点数据直接以表的形式存储到redis，这极大的提高了服务器响应速度，这样我们的api可直接获取redisgraph中的表数据。

## 6. 文档
[python 客户端](https://github.com/RedisGraph/redisgraph-py)

[查询文档示例](https://github.com/Liangchengdeye/redisGraphApp/blob/master/data/redisGraph%E5%88%86%E4%BA%AB.pptx)

pip install redisgraph
