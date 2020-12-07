# 下一步看什么

为了使 Django 的文档达到更易使用，更易阅读，更加全面的目的，我们付出了巨大的努力。本文档的剩余部分将更详细地介绍此文档的工作方式，以便您可以充分利用它。

（是的，这就是传说中的说明文档的说明文档。请放心，我们不打算写一篇关于如何阅读此文档的文档。）

## 文档是如何组成

Django 有丰富的文档。一份高度概述的文档会告诉你在哪里找到特定的东西：

- [教程](https://docs.djangoproject.com/zh-hans/2.2/intro/) 通过手把手地方式教你一步步的创建一个 Web 应用。如果你初学 Django 或编程，请从这里开始。
- [专题指南](https://docs.djangoproject.com/zh-hans/2.2/topics/) 在相当高的层次上介绍关键主题和概念，并提供有用的背景信息和解释。
- [参考指南](https://docs.djangoproject.com/zh-hans/2.2/ref/) 包含 API 和 Django 各个工作机制方面的技术参考。它们介绍了 Django 是如何工作，如何被使用的。不过，你得先对关键字的概念有一定理解。
- [操作指南](https://docs.djangoproject.com/zh-hans/2.2/howto/) 是一份目录。它们以排列好的关键问题和用例的方式指导你。它们比教程更加深入，且需要你先了解一些关于 Django 是如何工作的知识。

## 从哪里获取这个

你可以以好几种形式阅读 Django 的文档。他们按照优先顺序排列：

### 在网络上

Django 最新的在线版文档位于 https://docs.djangoproject.com/en/dev/。这些网页由 Django 的源码控制系统中的纯文本文件自动生成。

### 纯文本形式

离线阅读，或仅仅是为了方便，你可以阅读 Djano 文档的纯文本形式。

如果你正在使用的是 Django 的某个正式发布版，注意有一个代码压缩包，包含了 docs/ 目录，内含这个版本的完整文档。

一种没啥技术含量的利用纯文本文档的方式是使用 Unix 的 grep 工具在文档中全局中搜索一个短语。举个例子，接下来会向你展示 Django 文档中所有提到这个特定短语 "max_length" 的地方：

`grep -r max_length /path/to/django/docs/`

### 以本地网页形式阅读

经过几步简单的操作，你可以获得一份网页文档的备份：

- Django 文档使用了一个叫做 Sphinx 的系统将纯文本转换为网页。你可以通过 Sphinx 的官方网站或 pip 来下载和安装它：

`pip install Sphinx`

- 接着，仅需使用其中的 Makefile 工具将文档转换为网页：
```text
$ cd path/to/django/docs
$ make html
```

你需要为此安装 GNU Make 工具。

如果你是 Windows 系统，你应该使用其中的批处理文件：

```text
cd path\to\django\docs
make.bat html
```

- 这个 HTML 文档将会被放置在 docs/_build/html。


