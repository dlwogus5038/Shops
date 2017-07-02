from django.db import models

# Create your models here.
from django.utils import timezone


class ShopManager(models.Manager):
    def get_by_natural_key(self, urlID):
        return self.get(urlID=urlID)

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
        return "{}: id: {}, 位置: {}, 分类: {}, 味道: {}, 服务: {}, 环境: {}".format(self.shopname, self.id,
                                                     self.loc, self.foodtype, self.taste, self.service, self.envi)

'''class Region(models.Model):
    """
    regions' data structure
    one restaurant may belongs to several regions, e.g. Haidian region, Zhongguancun,
    meanwhile, one region may contain many shops
    """
    name = models.CharField(max_length=20)
    restaurant = models.ManyToManyField(Restaurant)

    def __str__(self):
        return "{}: id{}".format(self.name, self.id)


class Category(models.Model):
    """
    restaurant categories' class
    as for file 'restaurant', similar to Region
    """
    name = models.CharField(max_length=20)
    restaurant = models.ManyToManyField(Restaurant)

    def __str__(self):
        return "{}: id{}".format(self.name, self.id)'''


class Comment(models.Model):
    """
    reviews' class
    one restaurant may have many reviews, but one review only belongs to one restaurant
    same for the 'user' field
    """
    content = models.TextField(max_length=1000)
    shop = models.ForeignKey(Shop)  # shop's urlID
    # user = models.ForeignKey('User')  # TO DO: check with the User's developer
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "id{}, {}".format(self.id, self.created_at)









