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

main分支 🌹

### 项目初始化

#!!!!注意第一步不要迁移数据库！！！#

🈲️ python manage.py makemigrations & python manage.py migrate

首先你需在你的 settings.py: INSTALLED_APPS 中加入以下两个drf必须的app

- rest_framework 是为了把drf框架引入到你的项目

- rest_framework.authtoken 会在你第一次迁移数据库的时候生成用户Token表


```python

INSTALLED_APPS = [
    'rest_framework',
    'rest_framework.authtoken'
]

```

接下来把下面的 REST_FRAMEWORK 拷贝到你的setting.py文件中，里边包含了一些drf的基本配置

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

数据库的设置Django默认数据库为sqlite 你可以把他换成你的mysql数据库，只需要简单的配置 settings.py: DATABASES 即可

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'DRF_TEST1',
        'USER': 'root',
        'PASSWORD': '12345678',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}
```
配置完DATABASE之后，你需要在你的项目初始文件夹的__init__.py中添加以下内容，以确保连接数据库

DRF_Professional/__init__.py

```python
import pymysql
pymysql.install_as_MySQLdb()
```

至此基本配置完成✅✅✅✅✅


### 第一个APP：User

Django框架在你第一次进行数据库迁移的时候会默认给你生成User表

当然你也可以继承默认User表来创建自己的User表

首先你需要先start一个 user app：python manage.py startapp user

之后将此app注册到你的setting.py: INSTALLED_APPS中

在user/models.py中写入以下代码来创建你的user表：

可添加额外你所需要字段

```python

SEX_CHOICES = [
    (1, '男'),
    (2, '女')
]

class User(AbstractUser):
    nickname = models.CharField(
        max_length=150
    )
    sex = models.IntegerField(
        choices=SEX_CHOICES
    )

    def __str__(self):
        return self.nickname

    class Meta:
        # 默认id升序排序
        ordering = ['-id']
        # 数据库表名
        db_table = 'user'
```

至此 可进行第一次数据库迁移 ✌️ ✌️

**可前往apps/user/views.py 中查看万能注册、登录接口**

#### 注册接口的实现

首先你需要定义好自己的注册序列化器

apps/user/serializer.py

```python

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)
    username = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'username',
            'password',
            'confirm_password',
            'sex',
            'code'
        ]

    default_error_messages = {
        'code_error': '验证码不正确',
        'password_error': '两次密码输入不正确',
        "username_error": '手机号码格式不正确',
    }

    def validate(self, attrs):
        if not re.match(r'^1[3-9]\d{9}$', attrs['username']):
            raise ParamsException(self.error_messages['username_error'], 422)
        if attrs.get('code') != '123':
            raise ParamsException(self.error_messages['code_error'], 422)
        if attrs.get('password') != attrs.get('confirm_password'):
            raise ParamsException(self.error_messages['password_error'], 422)
        del attrs['confirm_password']
        del attrs['code']
        attrs['password'] = make_password(attrs['password'])
        return attrs
```

因为注册需要将信息写入到User表中，所以该序列化器继承自 serializers.ModelSerializer

此序列化器主要是对注册字段的校验，所以重写了validate方法

主要校验的字段为 username password confirm_password code(短信验证码)，所以将他们定义到了序列化器中并对其在validate方法中进行了校验

ParamsException异常为自定义异常 utils/exception.py, 同时自定义了drf异常捕获

**定义好之后需要加在settings.py：REST_FRAMEWORK中**

```python
REST_FRAMEWORK = {
    # 异常返回格式控制
    'EXCEPTION_HANDLER': 'utils.exception.custom_exception_handler',
}
```

apps/user/views.py

```python
class UserSignupAPIView(CreateAPIView):
    serializer_class = UserSignupSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.instance

        Token.objects.get_or_create(user=user)
        data = {"code": 200, "msg": "成功"}

        return Response(
            data=data,
            status=status.HTTP_201_CREATED
        )
```
注册api继承了generics的CreateAPIView，在这里你可以重写post方法来定制你自己的api， 注册成功将Token记录到表中

Token表：from rest_framework.authtoken.models import Token


#### 登录接口的实现

apps/user/serializer.py

```python
class UserSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': '用户已被禁用',
        'invalid_credentials': '账号或密码无效'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise ParamsException(self.error_messages['inactive_account'], 404)
            return attrs
        else:
            raise ParamsException(self.error_messages['invalid_credentials'], 404)
```

因为登录主要校验username和password的真实性，所以此序列化器继承自serializers.Serializer，重写__init__方法加入user，使其序列化成功后可携带user信息

重写validate方法完成username和password的校验

apps/user/views.py

```python
class UserSigninAPIView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user

        token, _ = Token.objects.get_or_create(user=user)
        data = {"code": 200, "msg": "成功", "data": {"token": token.key, "nickname": user.nickname}}

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )
```
api接口继承自GenericAPIView基础类，并重写post方法完成登录的校验
