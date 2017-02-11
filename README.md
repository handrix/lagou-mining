拉勾网数据挖掘
======

背景
---
毕业设计，大概构想为两个模块，即数据抓取与挖掘，抓取方面将重度依赖`scrapy`框架，
挖掘方面则是使用`sklearn`工具包，站在巨人的肩膀上，绝不重复造轮子。

技术栈
--
- 数据抓取-scrapy
- 代理池-redis
- db层-mongodb
- 挖掘工具-sklearn

安装文档
---
本来叫我撸文档我是拒绝的，但是想到我们走了之后学弟学妹们还有可能接着填这个坑，我就顺手撸一份吧。
### spider
    spider部分主要依赖scrapy框架所以安装完scrapy你就基本完成了该文档的50%任务啦(⊙o⊙)
    首先保证你的系统为`*unix`系统，在确认安装了`python`的前提下，btw：基本主流发行版都会有`python`
    的，在终端输入`python`验证，如果成功进入python命令行则证明成功。注意：版本选择2.7.10+

- scrapy
```
    sudo pip install scrapy
```

- redis
```
    sudo apt-get update
    sudo apt-get install redis-server
```

- mongodb
```
    sudo apt-get install mongo
    pip install mongoengine
    此外建议下载robomango作为可视化工具，这个google/baidu即可，安装方法不在此赘述
```

### sklearn

```
    sudo pip install sklearn
```