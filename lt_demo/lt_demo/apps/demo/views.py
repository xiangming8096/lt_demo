import json
from django.db import models
from django.views import View


class InsertView(View):
    def post(self, request):
        # 提取json数据
        response_json = json.loads(request.body.decode())

        # 分离json数据
        name = response_json.get('name')
        age = response_json.get('age')
        temp = response_json.get('temp')
