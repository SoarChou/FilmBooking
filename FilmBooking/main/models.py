from typing import Collection
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey

# Create your models here.

class User(models.Model):
    '''用户表'''
    user_id = models.AutoField(primary_key=True)
    gender = (
        ('male','男'),
        ('female','女'),
    )
 
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    # 时间戳
    c_time = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.name
    
    # model的内部类，定义表属性信息
    class Meta:
        # 排序依据
        ordering = ['c_time']
        # 表名
        verbose_name = '用户'
        # 表名复数形式
        verbose_name_plural = verbose_name

class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128,unique=True)
    password = models.CharField(max_length=256)
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        # 排序依据
        ordering = ['c_time']
        # 表名
        verbose_name = '管理员'
        # 表名复数形式
        verbose_name_plural = verbose_name

class Movie(models.Model):
    movie_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256,unique=True)
    # 封面链接
    cover = models.URLField(max_length=200)
    c_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    class Meta:
        # 排序依据
        ordering = ['-c_time']
        # 表名
        verbose_name = '电影'
        # 表名复数形式
        verbose_name_plural = verbose_name

class MovieTag(models.Model):
    tags = (
        ("hy","华语"),
        ("om","欧美"),
        ("rh","日韩"),
        ("dz","动作"),
        ("xj","喜剧"),
        ("aq","爱情"),
        ("kh","科幻"),
        ("xy","悬疑"),
        ("kb","恐怖"),
        ("wy","文艺"),
    )
    tag_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey("Movie", on_delete=models.CASCADE)
    tag = models.CharField(max_length=32,choices=tags)
    class Meta:
        # 排序依据
        ordering = ['movie_id']
        # 表名
        verbose_name = '标签'
        # 表名复数形式
        verbose_name_plural = verbose_name

class Cinema(models.Model):
    cinema_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128,unique=True)
    # 简介
    detail = models.CharField(max_length=384)
    # 地址
    position = models.CharField(max_length=384)
    def __str__(self):
        return self.name
    class Meta:
        # 排序依据
        ordering = ['cinema_id']
        # 表名
        verbose_name = '影院'
        # 表名复数形式
        verbose_name_plural = verbose_name

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    cinema_id = models.ForeignKey("Cinema", on_delete=models.CASCADE)
    # 房间号
    num = models.IntegerField()
    # 行
    col = models.IntegerField()
    # 列
    row = models.IntegerField()
    def __str__(self):
        return self.num
    class Meta:
        # 排序依据
        ordering = ['room_id']
        # 表名
        verbose_name = '影厅'
        # 表名复数形式
        verbose_name_plural = verbose_name

class Schedule(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    movie_id = models.ForeignKey("Movie", on_delete=models.CASCADE)
    room_id = models.ForeignKey("Room", on_delete=models.CASCADE)
    date = models.DateField(null=False)
    # 开始时间
    start_time = models.TimeField(null=False)
    # 价格
    price = models.DecimalField(max_digits=4, decimal_places=2)
    class Meta:
        # 排序依据
        ordering = ['schedule_id']
        # 表名
        verbose_name = '排期'
        # 表名复数形式
        verbose_name_plural = verbose_name

class Ticket(models.Model):
    states = (
        ("using","待使用"),
        ("used","已使用"),
        ("returned","已退票"),
    )
    ticket_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("User", on_delete=models.CASCADE)
    schedule_id = models.ForeignKey("Schedule", on_delete=models.CASCADE)
    seat_col = models.IntegerField()
    seat_row = models.IntegerField()
    state = models.CharField(max_length=32, choices=states)

    class Meta:
        # 排序依据
        ordering = ['ticket_id']
        # 表名
        verbose_name = '影票'
        # 表名复数形式
        verbose_name_plural = verbose_name

