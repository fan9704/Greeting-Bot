from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class User(models.Model):
    first_name = models.CharField(max_length=255, default="", verbose_name="名字")
    last_name = models.CharField(max_length=255, default="", verbose_name="姓氏")
    gender = models.CharField(
        max_length=1,
        choices=(
            ('m', 'Male'),
            ('f', 'Female'),
        ),
        verbose_name='性別',
    )
    date_of_birth = models.DateField(
        verbose_name="生日",
        default=timezone.now,
    )
    email = models.EmailField(
        verbose_name="電子信箱"
    )

    def __str__(self):
        return "{}".format(self.email)
