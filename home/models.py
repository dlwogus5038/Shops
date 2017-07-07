from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser, User, UserManager
from django.db.models.signals import post_save
from types import MethodType #类动态绑定方法
import os

AVATAR_ROOT = 'static/media/avatar'
AVATAR_DEFAULT = os.path.join(AVATAR_ROOT, 'default.jpg')


class ShopManager(models.Manager):
    def get_by_natural_key(self, urlID):
        return self.get(urlID=urlID)

    def count_occurrence(self, classify_by):
        """
        custom query function which count the occurrence times of each distinct value in a specified classify_by
        the 'classify_by' input should be a column name(string)
        this return a list like:
        [('中餐', 24), ('西餐', 12), ...]
        """
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT " + classify_by + ", count(*) num FROM home_shop GROUP BY " + classify_by)
            result = list(cursor.fetchall())
            result = sorted(result, key=lambda x: -x[1])
        return result


class Shop(models.Model):
    """
    shops' data structure
    """
    objects = ShopManager()

    urlID = models.BigIntegerField(default=0)
    loc = models.CharField(max_length=50)
    tel = models.CharField(max_length=20, default="")
    pic = models.URLField(default="")
    shopname = models.CharField(max_length=50)
    service = models.FloatField(default=0)
    taste = models.FloatField(default=0)
    foodtype = models.CharField(max_length=50)
    shoplevel = models.CharField(max_length=50)
    envi = models.FloatField(default=0)
    avgcost = models.IntegerField(default=0.0)
    street_address = models.CharField(default="", max_length=50)

    class Meta:
        unique_together = (('urlID',),)

    def __str__(self):
        return "{}: id: {}, 位置: {}, 分类: {}".format(self.shopname, self.id, self.loc, self.foodtype)


class MyUserManager(UserManager):  # natural key
    def get_by_natural_key(self, username):
        return self.get(username=username)


class MyUser(AbstractUser):
    objects = MyUserManager()

    name = models.CharField(u'姓名', max_length=32, blank=True, null=False, default="无名")
    gender = models.CharField(u'性别', max_length=1, default='男')
    latitude = models.FloatField(u'纬度', default=40.0, null=False)
    longitude = models.FloatField(u'经度', default=116.33, null=False)
    friend = models.ManyToManyField('self', verbose_name='friend')
    avatar = models.ImageField(upload_to=AVATAR_ROOT,default="default.jpg")
    collect_shop = models.ManyToManyField(Shop, verbose_name="收藏店铺列表")
    last_visit_shop_id = models.IntegerField(default=19455366)

    class Meta:
        db_table = 'MyUser'
        verbose_name = u'用户'
        verbose_name_plural = u'用户'
        # unique_together = (('username',),)

    def __str__(self):
        return self.username


class Request_Friend(models.Model):
    to_user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    from_user = models.CharField(u'好友ID', max_length=32, blank=True, null=False, default="无ID")

    class Meta:
        db_table = 'Request_Friend'
        verbose_name = u'给我申请的好友'
        verbose_name_plural = u"给我申请的好友"


class Comment(models.Model):
    """
    comments' class
    one shop may have many reviews, but one review only belongs to one shop
    same for the 'user' field
    
    NOTE: since Comment has a foreign key referencing MyUser, we need to add natural key handling to users' class
    see https://docs.djangoproject.com/en/1.11/topics/serialization/#natural-keys for detail
    """
    content = models.TextField(max_length=1000)
    shop = models.ForeignKey(Shop)  # shop's id
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)  # user's id
    username = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "id: {}, 用户: {}, 创建时间: {}, 对应店铺id: {}".format(self.id, self.username, self.created_at, self.shop_id)









