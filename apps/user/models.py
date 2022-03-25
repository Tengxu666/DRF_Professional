from django.contrib.auth.models import AbstractUser
from django.db import models

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

    # 只读属性
    @property
    def name(self):
        return self.nickname

    def __str__(self):
        return self.username

    class Meta:
        # 默认id升序排序
        ordering = ['-id']
        # 数据库表名
        db_table = 'user'
