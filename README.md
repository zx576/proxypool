# proxypool

基于 django 制作的 IP 池，本项目使用 requests+bs4 爬取数据，依托 django 数据库系统保存，通过网络请求从数据库内获取 IP，运行中有疑问可以在 Issues 下
提交。

该 IP 池已经在线部署到以下地址：lab.crossincode.com/proxy

## 运行环境

- python 3+
- django 1.10
- linux/windows

## 运行依赖包

- requests
- bs4
- lxml
- selenium
- PhantomJS

## 下载使用

`git clone https://github.com/zx576/proxypool.git`

进入项目文件夹

创建超级用户

`python manage.py createsuperuser`

依次输入用户名和密码即可

## 运行 django 项目

`$ python manage.py runserver`

访问首页
http://127.0.0.1:8000/proxy/

### 运行爬虫任务
#### 1、windows 下计划任务

将 sche_spider.py 加入计划任务

参考:http://mp.weixin.qq.com/s/JKFvnmtlEqaE8GxbX6Fpyw

#### 2、linux-cron

命令行下

`$ crontab -e `

添加计划任务，示例

`0 */4 * * *  python3 run_spider.py`

表示每 4 个小时运行一遍爬取任务


#### 2、手动运行

进入项目文件夹

`$ python manage.py runserver`

进入 http://127.0.0.1:8000/proxy/work/
手动点击 crwal 按钮运行


## 项目说明

### 爬取 IP

#### 爬取流程

请求网站 --> 获得代理 --> 存入数据库

#### 文件说明

爬虫文件在 spider 文件夹下
验证、去重整理等文件在 utils 文件夹下

#### 目前爬取的网站

- IP181
- 快代理
- 66 代理
- 西刺代理

#### 扩展网站

- 爬虫脚本编写参考爬虫文件
- 脚本编写好之后，在 utils 文件夹下 fetch.py 中导入该文件主函数，加入线程池即可

### 验证 IP

#### 文件说明

验证 IP 文件在 utils 文件夹下 VerifyProxy.py

#### 验证流程

请求 3 个网站，至少通过 2 次 --> 验证成功

### 整理 IP

#### 文件说明

整理数据库内 IP 的文件为 utils 文件夹下的 SortDt.py

#### 整理流程

清除重复的 IP

### API 提取 IP 接口

#### API 提取 url

- 默认返回 5 个，最多 20
- 请求频率为 3 秒一次，频繁请求不会返回内容

运行项目

`$ python manage.py runserver`

API 地址

http://127.0.0.1:8000/proxy/get/

在线地址：http://lab.crossincode.com/proxy/get/

#### 参数

| name      | type | Description | Optional | example | Remarks |
| :-------- | --------:| :------: | :------: | :------: | :------: |
| num    |   int |  IP 数量  |   可选 |  10  |每次最多20  | 默认 5 个 |
| v_num    |   int |  验证通过次数  |   可选 |  5  |原则上通过次数，越多IP越稳定，次数越大IP数量越少 |
| type    |   str |  ip类型  |   可选 |  O  |  G-'高匿',T-'透明',O-'其他'|
| head    |   str |  http 或者 https  |   可选 |  https  |  默认为 http|
| loc    |   str |  地区  |   可选 |  上海  |尽量以省市一级的地名查询  |

示例: http://127.0.0.1:8000/proxy/get/?num=10&v_num=5&head=https&loc=上海

在线地址: http://lab.crossincode.com/proxy/get/?num=10&v_num=5&head=https&loc=上海


说明: 提取10个ip , 通过验证次数大于等于 5，https 类型，ip坐标上海

### 查看数据库情况

#### django自带的admin

启动 django 项目之后，进入网页

http://127.0.0.1:8000/proxy/admin

#### 可视化图表

结合 echarts 做了可视化图表

地址:http://127.0.0.1:8000/proxy/chart/
