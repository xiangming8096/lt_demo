from django.db import models


class BaseModel(models.Model):
    """创建基类"""
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 更新时间
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    # 类属性
    class Meta:
        # 抽象模型类, 不会创建表
        abstract = True


class Area(models.Model):
    """地区表"""

    # 城市名称
    name = models.CharField(max_length=20, verbose_name='名称')

    # 上级id
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs', null=True,
                               blank=True, verbose_name='上级行政区划')

    class Meta:
        db_table = 'tb_areas'
        verbose_name = '行政区划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class UserInfo(models.Model):
    """用户信息表"""
    # 姓名
    name = models.CharField(max_length=10, verbose_name='姓名')
    # 年龄
    age = models.IntegerField(null=True, verbose_name='年龄')
    # 体温
    temp = models.FloatField(verbose_name='体温')
    # 地址 - 省
    province = models.ForeignKey(Area,
                                 on_delete=models.PROTECT,
                                 related_name='province_addresses',
                                 verbose_name='省')
    # 地址 - 市
    city = models.ForeignKey(Area,
                             on_delete=models.PROTECT,
                             related_name='city_addresses',
                             verbose_name='市')
    # 地址 - 区
    district = models.ForeignKey(Area,
                                 on_delete=models.PROTECT,
                                 related_name='district_addresses',
                                 verbose_name='区')

    def __str__(self):
        return self.name

