初识 Django
===========

Django 最初被设计用于具有快速开发需求的新闻类站点，目的是要实现简单快捷的网站开发。以下内容简要介绍了如何使用 Django 实现一个数据库驱动的 Web 应用。


设计模型
============

```
from django.db import models

class Reporter(models.Model):
    full_name = models.CharField(max_length=70)

    def __str__(self):
        return self.full_name

class Article(models.Model):
    pub_date = models.DateField()
    headline = models.CharField(max_length=200)
    content = models.TextField()
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.headline

```

应用数据模型
============

.. console::

    $ python manage.py makemigrations
    $ python manage.py migrate

该 makemigrations 命令查找所有可用的models，为任意一个在数据库中不存在对应数据表的model创建 migrations 脚本文件。migrate 命令则运行这些 migrations 自动创建数据库表。还提供可选的 更丰富的控制模式。