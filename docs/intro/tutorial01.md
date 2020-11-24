# 编写你的第一个 Django 应用，第 1 部分

创建一个基本的投票应用程序。

它将由两部分组成：
- 一个让人们查看和投票的公共站点。
- 一个让你能添加、修改和删除投票的管理站点。


## 创建项目

` django-admin startproject qiaosite`

## 用于开发的简易服务器

` python manage.py runserver`

## 创建投票应用

> 项目 VS 应用

```项目 VS 应用

项目和应用有什么区别？应用是一个专门做某件事的网络应用程序——比如博客系统，或者公共记录的数据库，或者小型的投票程序。项目则是一个网站使用的配置和应用的集合。项目可以包含很多个应用。应用可以被很多个项目使用。
```


## 创建一个应用：


在你的 manage.py 同级目录下创建投票应用。这样它就可以作为顶级模块导入，而不是 mysite 的子模块。

`python manage.py startapp polls`
这将会创建一个 polls 目录，它的目录结构大致如下：
```

D:\PyCharmWorkSpace\learn-django\qiaosite\polls>tree /F
文件夹 PATH 列表
卷序列号为 828B-9344
D:.
│  admin.py
│  apps.py
│  models.py
│  tests.py
│  views.py
│  __init__.py
│
└─migrations
        __init__.py

```
这个目录结构包括了投票应用的全部内容。

## 编写第一个视图

打开 polls/views.py，把下面这些 Python 代码输入进去：

```
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

```
这是 Django 中最简单的视图。如果想看见效果，我们需要将一个 URL 映射到它——这就是我们需要 URLconf 的原因了。

为了创建URLconf，请在polls目录里新建一个urls.py文件，目录结构是这样的：
```text

D:\PyCharmWorkSpace\learn-django\qiaosite\polls>tree /F
文件夹 PATH 列表
卷序列号为 828B-9344
D:.
│  admin.py
│  apps.py
│  models.py
│  tests.py
│  urls.py
│  views.py
│  __init__.py
│
├─migrations
│      __init__.py
│
└─__pycache__
        urls.cpython-36.pyc
        views.cpython-36.pyc
        __init__.cpython-36.pyc


D:\PyCharmWorkSpace\learn-django\qiaosite\polls>


```
在 polls/urls.py中，输入如下代码：

```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

在根 URLconf 文件中指定我们创建的 polls.urls 模块。在 qiaosite/urls.py 文件的 urlpatterns 列表里插入一个 include()， 如下：

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

设计 include() 的理念是使其可以即插即用。
> 当包括其它 URL 模式时你应该总是使用 include() ， admin.site.urls 是唯一例外。

浏览器访问 http://localhost:8000/polls/，你应该能够看见 "Hello, world. You're at the polls index." ，这是你在 index 视图中定义的。

函数 path() 具有四个参数，两个必须参数：route 和 view，两个可选参数：kwargs 和 name。

- route 是一个匹配 URL 的准则（类似正则表达式）。当 Django 响应一个请求时，它会从 urlpatterns 的第一项开始，按顺序依次匹配列表中的项，直到找到匹配的项。
  
  这些准则不会匹配 GET 和 POST 参数或域名。例如，URLconf 在处理请求 https://www.example.com/myapp/ 时，它会尝试匹配 myapp/ 。处理请求 https://www.example.com/myapp/?page=3 时，也只会尝试匹配 myapp/。
- view 当 Django 找到了一个匹配的准则，就会调用这个特定的视图函数，并传入一个 HttpRequest 对象作为第一个参数，被“捕获”的参数以关键字参数的形式传入。稍后，我们会给出一个例子。
- kwargs 任意个关键字参数可以作为一个字典传递给目标视图函数。
- name 为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改一个文件就能全局地修改某个 URL 模式。

