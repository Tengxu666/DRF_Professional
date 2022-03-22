# DRF_Professional
有时候很苦恼自己的代码写的像一坨💩，立志最一枚高质量程序员🐛

👏欢迎来到我的DRF进阶之路💐💐

**Start From Today** ⛽️⛽️⛽️⛽️⛽️⛽️   2022.3.21 Monday

### 什么是DRF

这里引用一下官方文档的说明：

Django REST framework 框架是一个用于构建Web api的强大而灵活的工具包。  

优势:  
- Web可浏览API对开发人员来说是一个巨大的可用性优势。 
- 认证策略包括OAuth1a和OAuth2包。 
- 支持ORM和非ORM数据源的序列化。 
- 完全可定制——如果不需要更强大的特性，
- 只需使用常规的基于函数的视图。 广泛的文档和强大的社区支持。 
- 被国际公认的公司使用和信任，包括Mozilla, Red Hat, Heroku，和Eve

总而言之，我的感觉是相比较于Django来说Django REST framework的确是强大又灵活，直观的感受是在接口代码的编写中，强大的序列化器让你飘飘欲仙 👋

回归正传 🤌 look down 🧐

dev1分支 🌹

### 项目初始化

#### Setting.py

```python

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken'
]

```


```python

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 100,
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DEFAULT_RENDER_CLASSES': [
        'rest_framework.renders.JSONRenderer',
        'rest_framework.renders.BrowsableAPIRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ]
  }
```

