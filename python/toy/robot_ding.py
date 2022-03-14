import time
import hmac
import hashlib
import base64
import requests

"""
钉钉机器人

```bash
crontab -e
0 10 * * 1,2,3,4,5 python3 robot_ding.py
```
(crontab)[https://www.runoob.com/linux/linux-comm-crontab.html]
"""


class RobotDing:
    def __init__(self, app_secret, webhook):
        self.app_secret = app_secret
        self.webhook = webhook

    @staticmethod
    def getMillicSec() -> int:
        """
        时间戳/毫秒
        :return:
        """
        ts = time.time()
        return round(ts * 1000)

    def calcSign(self, nowMilliSec) -> str:
        """
        计算签名
        :param nowMilliSec:
        :return:
        """
        timestamp = nowMilliSec
        app_secret_enc = app_secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, app_secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        return sign

    def getData(self) -> dict:
        """
        组合数据
        :return:
        """
        data = {
            "msgtype": "text",
            "text": {
                "content": "今天打卡了吗?",
            },
            "at": {
                "atMobiles": [
                    "null"  # 要@对象的手机号
                ],
                "isAtAll": True  # 是否要@所有人
            }
        }
        return data

    def run(self) -> None:
        timestamp = self.getMillicSec()
        sign = self.calcSign(timestamp)
        url = f"{self.webhook}&timestamp={timestamp}&sign={sign}"
        post = requests.post(url, json=self.getData())
        print(post.text)


if __name__ == '__main__':
    app_secret = 'SEC0e74227d78fe70606bcd167046290066cb63b01541f7eb6d6fe34d16d73b5d81'
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=1d9867370fee9201ca067566ce7350725adccb810edcd5278a683b7856609acf"
    RobotDing(app_secret, webhook).run()
