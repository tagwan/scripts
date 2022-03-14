import requests
import json

"""
__author__: jdg
"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
}

MARKDOWN_TEXT = "#### {city}明日天气\n" \
                "> 9度，西北风1级，空气良89，相对温度73%\n\n" \
                "- 温度: {low}-{high}" \
                "- 日出时间: {sunrise}" \
                "- 日落时间: {sunset}" \
                "- 温馨提示: {notice}" \
                "> ![screenshot](https://gw.alicdn.com/tfs/TB1ut3xxbsrBKNjSZFpXXcXhFXa-846-786.png)\n" \
                "> ###### {updateTime}发布\n"

class MyClass:
    var_a: str
    var_b: str

class Weather(object):
    url = r"http://t.weather.itboy.net/api/weather/city/"

    def __init__(self, city_code) -> None:
        self.url = self.url + str(city_code)

    def fetchText(self) -> dict:
        response = requests.get(url=self.url, headers=HEADERS)
        text = response.text
        return json.loads(text)

    def validate(self, text) -> None:
        if not isinstance(text, dict):
            raise Exception("Invalid Type!", type(text))

        if text['status'] != 200:
            raise Exception("status", text['status'])

    def fetch_md(self, city, weather) -> str:
        lowList = weather['low'].split(" ")
        highList = weather['high'].split(" ")
        print(list)
        MARKDOWN_TEXT = f"#### {city['city']}-明日天气\n" \
                        f"> {weather['type']}，{lowList[1]}~{highList[1]}，{weather['fx']}{weather['fl']}\n" \
                        f"- 日出时间: {weather['sunrise']}\n" \
                        f"- 日落时间: {weather['sunset']}\n" \
                        f"- 温馨提示: {weather['notice']}\n" \
                        f"> ###### {city['updateTime']}发布\n"
        print(MARKDOWN_TEXT)
        return MARKDOWN_TEXT

    def run(self) -> None:
        """
        run
        :return:
        """
        response = self.fetchText()
        self.validate(response)
        cityInfo = response['cityInfo']
        print(cityInfo)
        data = response['data']['forecast']

        weather_info = data[1]
        print(weather_info)
        self.fetch_md(cityInfo, weather_info)


if __name__ == '__main__':
    Weather(101190401).run()
