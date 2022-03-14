import requests
import json
import datetime


def weather(city):
    url = "http://wthrcdn.etouch.cn/weather_mini?city=%s" % city

    try:
        data = requests.get(url).json()['data']
        city = data['city']
        ganmao = data['ganmao']

        today_weather = data['forecast'][0]
        res = "老婆今天是{}\n今天天气概况\n城市: {:<10}\n时间: {:<10}\n高温: {:<10}\n低温: {:<10}\n风力: {:<10}\n风向: {:<10}\n天气: {:<10}\n\n稍后会发送近期温度趋势图，请注意查看。\
            ".format(
            ganmao,
            city,
            datetime.datetime.now().strftime('%Y-%m-%d'),
            today_weather['high'].split()[1],
            today_weather['low'].split()[1],
            today_weather['fengli'].split('[')[2].split(']')[0],
            today_weather['fengxiang'], today_weather['type'],
        )

        return {"source_data": data, "res": res}
    except Exception as e:
        return str(e)


"""
获取天气预报趋势图
"""
# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import re
import datetime


def Future_weather_states(forecast, save_path, day_num=5):
    '''
    展示未来的天气预报趋势图
    :param forecast: 天气预报预测的数据
    :param day_num: 未来几天
    :return: 趋势图
    '''
    future_forecast = forecast
    dict = {}

    for i in range(day_num):
        data = []
        date = future_forecast[i]["date"]
        date = int(re.findall("\d+", date)[0])
        data.append(int(re.findall("\d+", future_forecast[i]["high"])[0]))
        data.append(int(re.findall("\d+", future_forecast[i]["low"])[0]))
        data.append(future_forecast[i]["type"])
        dict[date] = data

    data_list = sorted(dict.items())
    date = []
    high_temperature = []
    low_temperature = []
    for each in data_list:
        date.append(each[0])
        high_temperature.append(each[1][0])
        low_temperature.append(each[1][1])
        fig = plt.plot(date, high_temperature, "r", date, low_temperature, "b")

    current_date = datetime.datetime.now().strftime('%Y-%m')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.xlabel(current_date)
    plt.ylabel("℃")
    plt.legend(["高温", "低温"])
    plt.xticks(date)
    plt.title("最近几天温度变化趋势")
    plt.savefig(save_path)


"""
发送到企业微信
"""
# -*- coding: utf-8 -*-


import requests
import json


class DLF:
    def __init__(self, corpid, corpsecret):
        self.url = "https://qyapi.weixin.qq.com/cgi-bin"
        self.corpid = corpid
        self.corpsecret = corpsecret
        self._token = self._get_token()

    def _get_token(self):
        '''
        获取企业微信API接口的access_token
        :return:
        '''
        token_url = self.url + "/gettoken?corpid=%s&corpsecret=%s" % (self.corpid, self.corpsecret)
        try:
            res = requests.get(token_url).json()
            token = res['access_token']
            return token
        except Exception as e:
            return str(e)

    def _get_media_id(self, file_obj):
        get_media_url = self.url + "/media/upload?access_token={}&type=file".format(self._token)
        data = {"media": file_obj}

        try:
            res = requests.post(url=get_media_url, files=data)
            media_id = res.json()['media_id']
            return media_id
        except Exception as e:
            return str(e)

    def send_text(self, agentid, content, touser=None, toparty=None):
        send_msg_url = self.url + "/message/send?access_token=%s" % (self._token)
        send_data = {
            "touser": touser,
            "toparty": toparty,
            "msgtype": "text",
            "agentid": agentid,
            "text": {
                "content": content
            }
        }

        try:
            res = requests.post(send_msg_url, data=json.dumps(send_data))
        except Exception as e:
            return str(e)

    def send_image(self, agentid, file_obj, touser=None, toparty=None):
        media_id = self._get_media_id(file_obj)
        send_msg_url = self.url + "/message/send?access_token=%s" % (self._token)
        send_data = {
            "touser": touser,
            "toparty": toparty,
            "msgtype": "image",
            "agentid": agentid,
            "image": {
                "media_id": media_id
            }
        }

        try:
            res = requests.post(send_msg_url, data=json.dumps(send_data))
        except Exception as e:
            return str(e)


"""
main脚本
"""
# -*- coding: utf-8 -*-


from plugins.weather_forecast import weather
from plugins.trend_chart import Future_weather_states
from plugins.send_wechat import DLF
import os

# 企业微信相关信息
corpid = "xxx"
corpsecret = "xxx"
agentid = "xxx"
# 天气预报趋势图保存路径
_path = os.path.dirname(os.path.abspath(__file__))
save_path = os.path.join(_path, './tmp/weather_forecast.jpg')

# 获取天气预报信息
content = weather("大兴")

# 发送文字消息
dlf = DLF(corpid, corpsecret)
dlf.send_text(agentid=agentid, content=content['res'], toparty='1')

# 生成天气预报趋势图
Future_weather_states(content['source_data']['forecast'], save_path)
# 发送图片消息
file_obj = open(save_path, 'rb')
dlf.send_image(agentid=agentid, toparty='1', file_obj=file_obj)
