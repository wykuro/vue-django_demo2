from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Userinfo(models.Model):
    headImg = models.CharField(null=True, blank=True, max_length=300)
    nickName = models.CharField(null=True, blank=True, max_length=300)
    belong = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, )

    def __int__(self):
        return self.id


#
#
# class Category(models.Model):
#     name = models.CharField()
#     belong = models.ForeignKey('self')
#
#     def __int__(self):
#         return self.id


class Article(models.Model):
    title = models.CharField(null=True, blank=True, max_length=80)
    cover = models.CharField(null=True, blank=True, max_length=300)
    describe = models.CharField(null=True, blank=True, max_length=200)
    content = models.TextField()
    belong = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                               related_name='article_user')

    # belong = models.ForeignKey(Userinfo)

    def __int__(self):
        return self.id

# class Favourite(models.Model):
#     belong_user = models.ForeignKey(Userinfo)
#     belong_art = models.ForeignKey(Article)
#
#     def __int__(self):
#         return self.id


# class Like(models.Model):
#     belong_user = models.ForeignKey(Userinfo)
#     belong_art = models.ForeignKey(Article)
#
#     # num = models.IntegerField()
#
#     def __int__(self):
#         return self.id
#
#
# class PayOrder(models.Model):
#     order = models.CharField()
#     price = models.CharField()
#     status = models.BooleanField()
#
#     def __int__(self):
#         return self.id
