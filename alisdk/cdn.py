# -*- coding: utf8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkcdn.request.v20141111 import DescribeDomainFlowDataRequest
import config
import json
import datetime
import calendar

# 创建 AcsClient 实例
client = AcsClient(
    config.access_id,
    config.access_key,
    "cn-beijing"
)


def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month / 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)


def search(start_time, end_time):
    print (start_time, end_time)
    # 创建 request，并设置参数
    request = DescribeDomainFlowDataRequest.DescribeDomainFlowDataRequest()
    request.set_Interval(86400)
    request.set_StartTime(start_time)
    request.set_EndTime(end_time)
    # 发起 API 请求并打印返回
    response_json = client.do_action_with_exception(request)
    response = json.loads(response_json)
    total = 0.0
    for data_module in response['FlowDataPerInterval']['DataModule']:
        print (data_module['TimeStamp'], data_module['Value'])
        total += int(data_module['Value'])

    print(start_time, end_time, (total / 1024 / 1024 / 1024), 'GB')


from_date = datetime.datetime(2017, 1, 1)
end_date = datetime.datetime(2017, 7, 1)
i_date = from_date
while i_date <= end_date:
    j_date = add_months(i_date, 1)
    search(i_date.strftime('%Y-%m-%dT00:00Z'), j_date.strftime('%Y-%m-%dT00:00Z'))
    i_date = j_date
