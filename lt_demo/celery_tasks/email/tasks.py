from django.core.mail import send_mail
from django.conf import settings
from celery_tasks.main import celery_app
import json


@celery_app.task(name='ccp_send_sms_code')
def send_verift_email(email, data_dict):
    data_str = [f'体温:{key} >> {value}人<p></p>' for key, value in data_dict.items()]
    # 邮件标题
    subject = "每日体温汇总"

    # 邮件内容
    html_message = f'''
        <p>尊敬的用户您好！</p>
        <p>每日体温汇总情况如下</p>
        <p>{data_str}</p>
        
        '''

    # 发送邮件
    result = send_mail(subject, '', settings.EMAIL_FROM, [email], html_message=html_message)

    return result
