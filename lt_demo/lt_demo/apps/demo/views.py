import datetime
import json
import re

from django.db.models import Count
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache

from celery_tasks.email.tasks import send_verift_email
from demo.models import Area, UserInfo


# 省级数据
from settings.dev import EMAIL_ADDRESS


class ProvinceAreasView(View):
    def get(self, request):

        try:
            # 查询省级数据
            province_model_list = Area.objects.filter(parent__isnull=True)

            # 整理省级数据
            province_list = []
            for province in province_model_list:
                province_list.append({
                    "id": province.id,
                    "name": province.name
                })
            # 数据正常
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': cache.get('province_list')})

        except Exception as e:
            # 数据出错
            return JsonResponse({'code': 400, 'errmsg': '省份数据错误'})


# 市、区级数据
class SubAreasView(View):
    def get(self, request, pk):

        try:
            # 查询市\区数据
            sub_model_list = Area.objects.filter(parent=pk)

            # 查询省级数据
            parent = Area.objects.get(id=pk)

            # 市\区级数据
            subs = []

            for sub_model in sub_model_list:
                subs.append({'id': sub_model.id,
                             'name': sub_model.name})

            # 返回数据格式
            sub_data = {
                "id": parent.id,
                "name": parent.name,
                "subs": subs,
            }
            # 数据正常
            return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': sub_data})

        except Exception as e:
            # 数据失败
            return JsonResponse({'code': 400, 'errmsg': '城市或区县数据错误'})


class InsertView(View):
    def post(self, request):
        # 提取json数据
        request_json = json.loads(request.body.decode())

        # 分离json数据
        name = request_json.get('name')
        age = request_json.get('age')
        temp = request_json.get('temp')
        province = request_json.get('province')
        city = request_json.get('city')
        district = request_json.get('district')

        # 验证数据完整性
        if not all([name, age, temp, province, city, district]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        # 姓名年龄温度省市区单独验证 略
        # if not re.match('^\w{2,10}$', name):
        #     return JsonResponse({'code': 400, 'errmsg': 'name 格式错误'})

        # 保存用户信息
        try:
            userinfo = UserInfo.objects.create(name=name, age=age, temp=temp, province=province, city=city, district=district)
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '保存到数据库失败'})

        return JsonResponse({'code': 0, 'errmsg': f'{userinfo.name}：信息保存成功，时间：{userinfo.create_time}'})


# 查询数据


# 定时任务
def send_task_email():
    try:
        userinfo_list = UserInfo.objects.filter(create_time__gte=datetime.datetime.now().date()).values('temp').annotate(Count('name'))

    except Exception as e:
        return JsonResponse({'code': 400, 'errmsg': '数据库查询失败'})
    # 构建数据
    data_dict = {temp: name_count for temp, name_count in userinfo_list}

    # 发送邮件
    send_verift_email(EMAIL_ADDRESS, data_dict)
