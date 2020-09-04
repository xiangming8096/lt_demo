import datetime

from django.test import TestCase

# Create your tests here.
data_dict = {
    36.6: 12,
    324: 112
}
data_str = [f'体温:{key} >> {value}人<p>' for key, value in data_dict.items()]
print(data_str)

date = str(datetime.datetime.now().date())
date_time = datetime.datetime.strptime(f'{date} 00:00:00', '%Y-%m-%d %H:%M:%S')