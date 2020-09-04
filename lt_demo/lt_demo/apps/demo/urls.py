from django.urls import path
from . import views

urlpatterns = [
    path(r'^province_areas/$', views.ProvinceAreasView),  # 省级地址列表
    path(r'^sub_areas/$', views.SubAreasView),  # 市区级地址列表
    path(r'^insert/$', views.InsertView),  # 添加数据

]
