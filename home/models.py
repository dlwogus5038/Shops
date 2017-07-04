from django.db import models

# Create your models here.
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(u'姓名', max_length=32, blank=True, null=False , default="无名")
    gender = models.CharField(u'性别',max_length=1, default='男')
    latitude = models.FloatField(u'纬度',default = 40.0, null=False)
    longitude = models.FloatField(u'经度',default = 116.33, null=False)

    class Meta:
        db_table = 'Profile'
        verbose_name = u'用户详情'
        verbose_name_plural = u"用户详情"

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = UserProfile.objects.get(user=self.user)
                self.pk = p.pk
            except UserProfile.DoesNotExist:
                pass
        super(UserProfile, self).save(*args,**kwargs)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

post_save.connect(create_user_profile, sender=User)

class ProfileSite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userID = models.IntegerField(default=0)
    username = models.CharField(u'ID', max_length=32, blank=True, null=False, default="无名")
    name = models.CharField(u'姓名', max_length=32, blank=True, null=False, default="无名")
    email = models.EmailField(u'电子邮件地址',blank=True,null=False,default=".@.")
    gender = models.CharField(u'性别', max_length=1, default='男')
    latitude = models.FloatField(u'纬度', default=40.0, null=False)
    longitude = models.FloatField(u'经度', default=116.33, null=False)

    class Meta:
        db_table = 'ProfileSite'
        verbose_name = u'用户页面信息'
        verbose_name_plural = u'用户页面信息'

    def save(self, *args, **kwargs):
        if not self.pk:
            try:
                p = ProfileSite.objects.get(user=self.user)
                self.pk = p.pk
            except ProfileSite.DoesNotExist:
                pass
        super(ProfileSite, self).save(*args,**kwargs)

def create_profile_site(sender, instance, created, **kwargs):
    if created:
        profile_site = ProfileSite()
        profile_site.user = instance
        profile_site.username = instance.username
        profile_site.email = instance.email
        profile_site.save()

post_save.connect(create_profile_site, sender=User)


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


class Comment(models.Model):
    """
    comments' class
    one shop may have many reviews, but one review only belongs to one shop
    same for the 'user' field
    
    NOTE: since Comment has a foreign key referencing User, we need to add natural key handling to users' class
    see https://docs.djangoproject.com/en/1.11/topics/serialization/#natural-keys for detail
    """
    content = models.TextField(max_length=1000)
    shop = models.ForeignKey(Shop)  # shop's urlID
    # user = models.ForeignKey('User')  # TO DO: need to add this
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "id: {}, 创建时间: {}, 对应店铺id: {}".format(self.id, self.created_at, self.shop_id)









