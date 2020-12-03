# 进阶指南：如何编写可重用程序

我们将会把我们的 Web-poll 放进一个独立的 Python 包中，以便你在新的项目中重用它或将它与他人分享。

## 可重用性很重要

设计，构建，测试以及维护一个 web 应用要做很多的工作。很多 Python 以及 Django 项目都有一些常见问题。如果我们能保存并利用这些重复的工作岂不是更好？

可重用性是Python的生存方式。Django本身也只是一个Python包。这意味着您可以将现有的Python包或Django应用组合到您自己的Web项目中。您只需编写您项目独一无二的部分。

假设你现在创建了一个新的项目，并且需要一个类似我们之前做的投票应用。你该如何复用这个应用呢？庆幸的是，其实你已经知道了一些。在 教程 1，我们使用过 include 从项目级别的 URLconf 分割出 polls。在本教程中，我们将进一步使这个应用易用于新的项目中，并发布给其他人安装使用。

> 包？应用？
>> 一个 package 提供了一组关联的 Python 代码的简单复用方式。一个包（“模块”）包含了一个或多个 Python 代码文件。 
>> 
>> 一个包通过 import foo.bar 或 from foo import bar 的形式导入。一个目录（例如 polls）要成为一个包，它必须包含一个特定的文件 __init__.py，即便这个文件是空的。  
>> 
>> Django 应用 仅仅是专用于 Django 项目的 Python 包。应用会按照 Django 约定，创建好 models, tests, urls, 以及 views 等子模块。 

## 你的项目和可复用应用

通过前面的教程，我们的工程应该看起来像这样:

```text
├─qiaosite
│  │  db.sqlite3
│  │  manage.py
│  │
│  ├─polls
│  │  │  admin.py
│  │  │  apps.py
│  │  │  models.py
│  │  │  tests.py
│  │  │  urls.py
│  │  │  views.py
│  │  │  __init__.py
│  │  │
│  │  ├─migrations
│  │  │     0001_initial.py
│  │  │     __init__.py
│  │  │
│  │  ├─static
│  │  │  └─polls
│  │  │      │  style.css
│  │  │      │
│  │  │      └─images
│  │  │              background.jpg
│  │  ├─templates
│  │     └─polls
│  │             detail.html
│  │             index.html
│  │             results.html
│  ├─qiaosite
│  │  │  settings.py
│  │  │  urls.py
│  │  │  wsgi.py
│  │  │  __init__.py
│  ├─templates
│  │  └─admin
│  │          base_site.html
```

目录 polls 现在可以被拷贝至一个新的 Django 工程，且立刻被复用。不过现在还不是发布它的时候。为了这样做，我们需要打包这个应用，便于其他人安装它。

## 安装必须环境

目前，打包 Python 程序需要工具，有许多工具可以完成此项工作。在此教程中，我们将使用 setuptools 来打包我们的程序。这是推荐的打包工具（与 发布 分支合并）。我们仍旧使用 pip 来安装和卸载这个工具

## 打包你的应用

Python 的 打包 将以一种特殊的格式组织你的应用，意在方便安装和使用这个应用。Django 本身就被打包成类似的形式。对于一个小应用，例如 polls，这不会太难。

1. 首先，在你的 Django 项目目录外创建一个名为 learn-django-polls 的文件夹，用于盛放 polls。
2. 将 polls 目录移入 learn-django-polls 目录。
3. 创建一个名为 learn-django-polls/README.rst 的文件，包含以下内容：
4. 创建一个 learn-django-polls/LICENSE 文件
5. 创建setup.cfg和setup.py文件用于说明如何构建和安装应用的细节。
6. 默认包中只包含 Python 模块和包。为了包含额外文件，我们需要创建一个名为 MANIFEST.in 的文件。上一步中关于 setuptools 的文档详细介绍了这个文件。为了包含模板、README.rst 和我们的 LICENSE 文件，创建文件 learn-django-polls/MANIFEST.in 包含以下内容：
7. 在应用中包含详细文档是可选的，但我们推荐你这样做。创建一个空目录 learn-django-polls/docs 用于未来编写文档。额外添加一行至 learn-django-polls/MANIFEST.in  
   注意，现在 docs 目录不会被加入你的应用包，除非你往这个目录加几个文件。许多 Django 应用也提供他们的在线文档通过类似 readthedocs.org 这样的网站。
8. 试着构建你自己的应用包通过 ptyhon setup.py sdist （在 django-polls目录内）。这将创建一个名为 dist 的目录并构建你自己的应用包， learn-django-polls-0.1.tar.gz。

## 使用你自己的包名 

由于我们把 polls 目录移出了项目，所以它无法工作了。我们现在要通过安装我们的新 learn-django-polls 应用来修复这个问题。

1. 为了安装这个包，使用 pip:   
   `pip install --user django-polls/dist/django-polls-0.1.tar.gz`  
   注意： 在virtualenv 中安装，不要用--user 选项，这会安装到用户的python目录下。
2. 幸运的话，你的 Django 项目应该再一次正确运行。启动服务器确认这一点。
3. 通过 pip 卸载包:  
   `pip uninstall django-polls`
     
## 发布你的应用

现在，你已经对 learn django-polls 完成了打包和测试，准备好向世界分享它！   

将你的包发布至公共仓库，比如 the Python Package Index (PyPI)。 packaging.python.org 有一个不错的 教程 说明如何发布至公共仓库。  
 
## 通过 virtualenv 安装 Python 包

一般来说，这些状况只在你同时运行多个 Django 项目时出现。当这个问题出现时，最好的解决办法是使用 virtualenv。这个工具允许你同时运行多个相互独立的Python环境，每个环境都有各自库和应用包命名空间的拷贝。     