from django.db import models

# Create your models here.
from django.utils import timezone


class Shop(models.Model):
    """
    shops' data structure
    """
    shopurl = models.CharField(max_length=100)
    loc = models.CharField(max_length=20)
    shopname = models.CharField(max_length=50)
    service = models.FloatField(default=0)
    taste = models.FloatField(default=0)
    commentnum = models.IntegerField(default=0)
    foodtype = models.CharField(max_length=20)
    shoplevel = models.CharField(max_length=20)
    envi = models.FloatField(default=0)
    avgcost = models.IntegerField(default=0.0)

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
    content = models.TextField(max_length=2000)
    restaurant = models.ForeignKey(Shop)
    # user = models.ForeignKey('User')  # TO DO: check with the User's developer
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "id{}, {}".format(self.id, self.time)









