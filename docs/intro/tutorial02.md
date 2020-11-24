# 编写你的第一个 Django 应用，第 2 部分


## 数据库配置
 
 配置文件使用 SQLite 作为默认数据库。

 qiaosite/settings.py 。这是个包含了 Django 项目设置的 Python 模块
 
 编辑 qiaosite/settings.py 文件前，先设置 TIME_ZONE 为你自己时区。
 
 INSTALLED_APPS 设置项,这里包括了会在你项目中启用的所有 Django 应用。
 
  INSTALLED_APPS 默认包括了以下 Django 的自带应用：
  - django.contrib.admin -- 管理员站点， 你很快就会使用它。
  - django.contrib.auth -- 认证授权系统。
  - django.contrib.contenttypes -- 内容类型框架。
  - django.contrib.sessions -- 会话框架。
  - django.contrib.messages -- 消息框架。
  - django.contrib.staticfiles -- 管理静态文件的框架。

## 创建模型
这个简单的投票应用中，需要创建两个模型：问题 Question 和选项 Choice。Question 模型包括问题描述和发布时间。Choice 模型有两个字段，选项描述和当前得票数。每个选项属于一个问题。

这些概念可以通过一个简单的 Python 类来描述。按照下面的例子来编辑 polls/models.py 文件：

```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


```

每个模型被表示为 django.db.models.Model 类的子类。  
每个模型有一些类变量，它们都表示模型里的一个数据库字段。  
每个字段都是 Field 类的实例  

注意在最后，我们使用 ForeignKey 定义了一个关系。这将告诉 Django，每个 Choice 对象都关联到一个 Question 对象。Django 支持所有常用的数据库关系：多对一、多对多和一对一。

## 激活模型

创建模型的代码给了 Django 很多信息，通过这些信息，Django 可以：
- 为这个应用创建数据库 schema（生成 CREATE TABLE 语句）。
- 创建可以与 Question 和 Choice 对象进行交互的 Python 数据库 API。

但是首先得把 polls 应用安装到我们的项目里。

> **设计哲学**  
>> Django 应用是“可插拔”的。你可以在多个项目中使用同一个应用。除此之外，你还可以发布自己的应用，因为它们并不会被绑定到当前安装的 Django 上。


为了在我们的工程中包含这个应用，我们需要在配置类 INSTALLED_APPS 中添加设置。因为 PollsConfig 类写在文件 polls/apps.py 中，所以它的点式路径是 'polls.apps.PollsConfig'。在文件 qiaosite/settings.py 中 INSTALLED_APPS 子项添加点式路径后，它看起来像这样：

```python

# Application definition

INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

```   

现在你的 Django 项目会包含 polls 应用。接着运行下面的命令：

```text

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py makemigrations polls
Migrations for 'polls':
  polls\migrations\0001_initial.py
    - Create model Question
    - Create model Choice

```

通过运行 makemigrations 命令，Django 会检测你对模型文件的修改（在这种情况下，你已经取得了新的），并且把修改的部分储存为一次 迁移。  

Django 有一个自动执行数据库迁移并同步管理你的数据库结构的命令 - 这个命令是 migrate，我们马上就会接触它 - 但是首先，让我们看看迁移命令会执行哪些 SQL 语句。sqlmigrate 命令接收一个迁移的名称，然后返回对应的 SQL：

```python

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py sqlmigrate polls 0001
BEGIN;
--
-- Create model Question
--
CREATE TABLE "polls_question" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "question_text" varchar(200) NOT NULL, "pub_date" datetime NOT NULL);
--
-- Create model Choice
--
CREATE TABLE "polls_choice" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "choice_text" varchar(200) NOT NULL, "votes" integer NOT NULL, "question_id" integer NOT NULL REFERENCES "polls_question" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "polls_choice_question_id_c5b4b260" ON "polls_choice" ("question_id");
COMMIT;

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>

```

- 数据库的表名是由应用名(polls)和模型名的小写形式( question 和 choice)连接而来。（如果需要，你可以自定义此行为。）
- 主键(IDs)会被自动创建。(当然，你也可以自定义。)
- 默认的，Django 会在外键字段名后追加字符串 "_id" 。（同样，这也可以自定义。）

运行 migrate 命令，在数据库里创建新定义的模型的数据表：

```python

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, polls, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying polls.0001_initial... OK
  Applying sessions.0001_initial... OK

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>


```

迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表 - 它专注于使数据库平滑升级而不会丢失数据。我们会在后面的教程中更加深入的学习这部分内容，现在，你只需要记住，改变模型需要这三步：

- 编辑 models.py 文件，改变模型。
- 运行 python manage.py makemigrations 为模型的改变生成迁移文件。
- 运行 python manage.py migrate 来应用数据库迁移。

数据库迁移被分解成生成和应用两个命令是为了让你能够在代码控制系统上提交迁移数据并使其能在多个应用里使用；这不仅仅会让开发更加简单，也给别的开发者和生产环境中的使用带来方便。


## 初试 API

进入交互式 Python 命令行，尝试一下 Django 为你创建的各种 API。通过以下命令打开 Python 命令行：

```python

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py shell
Python 3.6.6rc1 (v3.6.6rc1:1015e38be4, Jun 12 2018, 08:38:06) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>

```

我们使用这个命令而不是简单的使用 "Python" 是因为 manage.py 会设置 DJANGO_SETTINGS_MODULE 环境变量，这个变量会让 Django 根据 mysite/settings.py 文件来设置 Python 包的导入路径。

```python

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py shell
Python 3.6.6rc1 (v3.6.6rc1:1015e38be4, Jun 12 2018, 08:38:06) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from polls.models import Choice, Question #Import the model classes we just wrote
>>> Question.objects.all()
<QuerySet []>
>>> from django.utils import timezone
>>> q = Question(question_text = "What's new", pub_date = timezone.now())
>>> q.save()
>>> q.id
1
>>> q.question_text
"What's new"
>>> q.question_test = "What's new?"
>>> q.save()
>>> q.question_text
"What's new"
>>> q.save()
>>> q.pub_date
datetime.datetime(2020, 11, 23, 10, 1, 8, 594896, tzinfo=<UTC>)
>>> q.question_test = "What's up?"
>>> q.save()
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
>>>

```

等等。<Question: Question object (1)> 对于我们了解这个对象的细节没什么帮助。让我们通过编辑 Question 模型的代码（位于 polls/models.py 中）来修复这个问题。给 Question 和 Choice 增加 __str__() 方法。

```python

from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete = models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

```

给模型增加 __str__() 方法是很重要的，这不仅仅能给你在命令行里使用带来方便，Django 自动生成的 admin 里也使用这个方法来表示对象。


让我们再为此模型添加一个自定义方法：