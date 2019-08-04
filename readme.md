# <div align="center"><a href="http://jzsc.mohurd.gov.cn/asite/jsbpp/index">全国建筑市场监管公共服务平台爬虫</a></div>

<div align="right">
@Author: 54fire  </br>
@Date:  2019-08-01  </br>
@Version: v1.0.0  
</div>

## 文件结构

- [build_spider]() - 文件目录
  - [core](./core) - 主要爬虫文件位置
    - building_spider
      - building_spider.py
      - project_spider.py
      - filter_project.py
      - detail_spider.py
      - save.py
    - db
      - redis.py
  - [config](./config) - 主要用来提供公司名，以及代理 ip
    - proxy
    - post_proxy
    - result
  - [temp](./temp) - 用来存放的临时文件, 方便排查错误
    - yes.txt
    - no.txt
  - [utils](./utils) - 为 requests 请求提供 headers
    - http.py
  - domain.py
  - settint.py
  - main.py - 程序入口

## 【Use】

1. 将可用的 ip 保存到`proxy`和`post_proxy`文件中, 且每一个之间站位一行, 格式为 `ip:port`
   例如：`123.23.34.42:2048`.

2. 修改`setting.py`中的配置文件，对爬虫需要的信息进行筛选

3. 运行`main.py`文件
