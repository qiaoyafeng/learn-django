# 编写你的第一个 Django 应用，第 5 部分

这一篇从 [教程第 4 部分](tutorial04.md) 结尾的地方继续讲起。我们在前几章成功的构建了一个在线投票应用，在这一部分里我们将为它创建一些自动化测试。

## 自动化测试简介

### 自动化测试是什么？

测试，是用来检查代码正确性的一些简单的程序。  
自动化 测试是由某个系统帮你自动完成的。当你创建好了一系列测试，每次修改应用代码后，就可以自动检查出修改后的代码是否还像你曾经预期的那样正常工作。你不需要花费大量时间来进行手动测试。

### 为什么你需要写测试

#### 测试将节约你的时间
在更加复杂的应用中，各种组件之间的交互可能会及其的复杂。改变其中某一组件的行为，也有可能会造成意想不到的结果。判断「代码是否正常工作」意味着你需要用大量的数据来完整的测试全部代码的功能，以确保你的小修改没有对应用整体造成破坏——这太费时间了。
#### 测试不仅能发现错误，而且能预防错误
「测试是开发的对立面」，这种思想是不对的。

#### 测试使你的代码更有吸引力
没有测试的代码不值得信任。项目规划时没有包含测试是不科学的。
#### 测试有利于团队协作
前面的几点都是从单人开发的角度来说的。复杂的应用可能由团队维护。测试的存在保证了协作者不会不小心破坏了了你的代码（也保证你不会不小心弄坏他们的）。如果你想作为一个 Django 程序员谋生的话，你必须擅长编写测试！

### 基础测试策略

一些开发者遵循 "测试驱动" 的开发原则，他们在写代码之前先写测试。这种方法看起来有点反直觉，但事实上，这和大多数人日常的做法是相吻合的。我们会先描述一个问题，然后写代码来解决它。「测试驱动」的开发方法只是将问题的描述抽象为了 Python 的测试样例。

## 开始写我们的第一个测试

### 首先得有个 Bug
我们的 polls 应用现在就有一个小 bug 需要被修复：我们的要求是如果 Question 是在一天之内发布的， Question.was_published_recently() 方法将会返回 True ，然而现在这个方法在 Question 的 pub_date 字段比当前时间还晚时也会返回 True（这是个 Bug）。

```python
Python 3.6.6rc1 (v3.6.6rc1:1015e38be4, Jun 12 2018, 08:38:06) [MSC v.1900 64 bit (AMD64)] on win32
Django 2.2.12
import datetime
from django.utils import timezone
from polls.models import Question
future_question = Question(pub_date=timezone.now() + datetime.timedelta(days=30))
future_question.was_published_recently()
True

```

因为将来发生的是肯定不是最近发生的，所以代码明显是错误的。

### 创建一个测试来暴露这个 bug

按照惯例，Django 应用的测试应该写在应用的 tests.py 文件里。测试系统会自动的在所有以 tests 开头的文件里寻找并执行测试代码。

将下面的代码写入 polls 应用里的 tests.py 文件内：

polls/tests.py
```python
import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() return False for questions whose pub_date is the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
```

我们创建了一个 django.test.TestCase 的子类，并添加了一个方法，此方法创建一个 pub_date 时未来某天的 Question 实例。然后检查它的 was_published_recently() 方法的返回值——它 应该 是 False。

### 运行测试

在终端中，我们通过输入以下代码运行测试:
`(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py test polls`

运行结果:
```python

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py test polls
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F
======================================================================
FAIL: test_was_published_recently_with_future_question (polls.tests.QuestionModelTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "D:\PyCharmWorkSpace\learn-django\qiaosite\polls\tests.py", line 16, in test_was_published_recently_with_future_question
    self.assertIs(future_question.was_published_recently(), False)
AssertionError: True is not False

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (failures=1)
Destroying test database for alias 'default'...

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>

```

发生了什么呢？以下是自动化测试的运行过程：

-    python manage.py test polls 将会寻找 polls 应用里的测试代码
-    它找到了 django.test.TestCase 的一个子类
-    它创建一个特殊的数据库供测试使用
-    它在类中寻找测试方法——以 test 开头的方法。
-    在 test_was_published_recently_with_future_question 方法中，它创建了一个 pub_date 值为 30 天后的 Question 实例。
-    接着使用 assertls() 方法，发现 was_published_recently() 返回了 True，而我们期望它返回 False。

测试系统通知我们哪些测试样例失败了，和造成测试失败的代码所在的行号。

### 修复这个 bug

我们早已知道，当 pub_date 为未来某天时， Question.was_published_recently() 应该返回 False。我们修改 models.py 里的方法，让它只在日期是过去式的时候才返回 True：

polls/models.py

```python

    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

```
运行测试:
```python
(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>python manage.py test polls
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
Destroying test database for alias 'default'...

(learn-django) D:\PyCharmWorkSpace\learn-django\qiaosite>

```
发现 bug 后，我们编写了能够暴露这个 bug 的自动化测试。在修复 bug 之后，我们的代码顺利的通过了测试。

将来，我们的应用可能会出现其他的问题，但是我们可以肯定的是，一定不会再次出现这个 bug，因为只要简单的运行一遍测试，就会立刻收到警告。我们可以认为应用的这一小部分代码永远是安全的。

### 更全面的测试

 was_published_recently() 已测试完成，事实上，在修复一个 bug 时不小心引入另一个 bug 会是非常令人尴尬的。
 
 在测试类里再增加两个测试，来更全面的测试这个方法：
 
polls/tests.py 

```python


    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() return False for questions whose pub_date is older than  1 day.
        """
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() return False for questions whose pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


```

现在，我们有三个测试来确保 Question.was_published_recently() 方法对于过去，最近，和将来的三种情况都返回正确的值。

## 测试视图
如果 pub_date 设置为未来某天，这应该被解释为这个问题将在所填写的时间点才被发布，而在之前是不可见的。

### 针对视图的测试

在我们的第一个测试中，我们关注代码的内部行为。我们通过模拟用户使用浏览器访问被测试的应用来检查代码行为是否符合预期。

在我们动手之前，先看看需要用到的工具们。

#### Django 测试工具之 Client

Django 提供了一个供测试使用的 Client 来模拟用户和视图层代码的交互。

第一步是在 shell 中配置测试环境:

```python
Python 3.6.6rc1 (v3.6.6rc1:1015e38be4, Jun 12 2018, 08:38:06) [MSC v.1900 64 bit (AMD64)] on win32
Django 2.2.12
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()

```
setup_test_environment() 提供了一个模板渲染器，允许我们为 responses 添加一些额外的属性，例如 response.context，未安装此 app 无法使用此功能。

导入Client包，并运行：
```python

Python 3.6.6rc1 (v3.6.6rc1:1015e38be4, Jun 12 2018, 08:38:06) [MSC v.1900 64 bit (AMD64)] on win32
Django 2.2.12
>>> from django.test.utils import setup_test_environment
>>> setup_test_environment()
>>> from django.test import Client
>>> client = Client()
>>> response = client.get('/')
Not Found: /
>>> response.status_code
404
>>> from django.urls import reverse
>>> response = client.get(reverse('polls:index'))
>>> response.status_code
200
>>> response.content
b'\n    <ul>\n    \n        <li><a href="/polls/2/">What&#39;s your name?</a></li>\n    \n        <li><a href="/polls/1/">What&#39;s new</a></li>\n    \n    </ul>\n'
>>> response.context['latest_question_list']
<QuerySet [<Question: What's your name?>, <Question: What's new>]>
>>> 
>>> 

```

#### 改善视图代码

现在的投票列表会显示将来的投票（ pub_date 值是未来的某天)。我们来修复这个问题。

ListView 的视图类：需要改进 get_queryset() 方法，让他它能通过将 Question 的 pub_data 属性与 timezone.now() 相比较来判断是否应该显示此 Question。

```python
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        :return: Return the last five published questions(not including those set to be published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


```

#### 测试新视图

写一个公用的快捷函数用于创建投票问题，再为视图创建一个测试类：

将下面的代码添加到 polls/tests.py ：

```python


from django.urls import reverse

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no quesions exist, an appropriate message displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )



```

让我们更详细地看下以上这些内容。

首先是一个快捷函数 create_question，它封装了创建投票的流程，减少了重复代码。

test_no_questions 方法里没有创建任何投票，它检查返回的网页上有没有 "No polls are available." 这段消息和 latest_question_list 是否为空。注意到 django.test.TestCase 类提供了一些额外的 assertion 方法，在这个例子中，我们使用了 assertContains() 和 assertQuerysetEqual() 。

在 test_past_question 方法中，我们创建了一个投票并检查它是否出现在列表中。

在 test_future_question 中，我们创建 pub_date 在未来某天的投票。数据库会在每次调用测试方法前被重置，所以第一个投票已经没了，所以主页中应该没有任何投票。

剩下的那些也都差不多。实际上，测试就是假装一些管理员的输入，然后通过用户端的表现是否符合预期来判断新加入的改变是否破坏了原有的系统状态。


#### 当需要测试的时候，测试用例越多越好
如果你对测试有个整体规划，那么它们就几乎不会变得混乱。下面有几条好的建议：

- 对于每个模型和视图都建立单独的 TestClass
- 每个测试方法只测试一个功能
- 给每个测试方法起个能描述其功能的名字


## 接下来要做什么？
当你已经比较熟悉测试 Django 视图的方法后，就可以继续阅读 [教程的第 6 部分](tutorial06.md)  ，学习静态文件管理的相关知识。