from lxml import etree
import requests
import pickle
import json
import bs4
import re
import os

class weather():
    def __init__(self, city):
        self.city = city
        if not os.path.exists('data.pkl'):
            self.get_cityCode()
        with open("data.pkl", "rb") as f:
            self.data = pickle.load(f)
            
        self.cityCode = self.data.get(self.city, None)
        if self.cityCode:
            if not re.match(r'[0-9]', self.cityCode):
                raise Exception("不支持查找整个省的天气，可尝试查找省会"+self.cityCode+"，或省内其他城市")
        else:
            raise Exception("查找不到该城市")
        
    # s = etree.HTML(html)
    # title = s.xpath('//*[@id="content"]/div/div[1]/div/table[1]/tbody/tr/td[2]/div/a')
    def get_cityCode(self):
        import pickle
        url = 'http://pc.weathercn.com/59086/?partner=&p_source=&p_type=jump'
        res = requests.get(url = url)
        js = res.text
        city = re.search(r"(?<=window\.nation_weather_map \= ).+", js).group()[:-1]
        city = json.loads(city,strict=False)
        data = {}
        for key,a in city.items():
            if a["other_city"]:
                data[key] = a['capital_name']
                data[a['capital_name']] = a["city_code"]
            else:
                data[key] = a["city_code"]
            for i in a["other_city"]:
                data[i["city_namecn"]] = i["city_code"]
        with open("data.pkl", "wb") as f:
            pickle.dump(data, f)

    def real_time_weather(self):
        url = 'http://pc.weathercn.com/weather/'+self.cityCode+'/?partner=&p_source=&p_type=jump&areatype='
        res = requests.get(url = url)
        print(res)
        html = res.text
        s = etree.HTML(html)

        data = {}

        date = {}
        date_key = ['Huang_Li',# 黄历列表 宜/忌
                'week',# 星期 星期一
                'lunar_calendar',# 农历 农历正月初十
                ]
        date_xpath = ['//*[@id="china-weather"]/div[1]/a/div/div[2]/p/text()',
                    '//*[@id="china-weather"]/div[1]/a/div/div[2]/p[1]/span/text()',
                    '//*[@id="china-weather"]/div[1]/a/div/div[2]/p[1]/text()']

        for i in range(3):
            if i == 0:
                date[date_key[i]] = s.xpath(date_xpath[i])[1:]
            else:
                date[date_key[i]] = s.xpath(date_xpath[i])[0]
        data["date"] = date

        weather = {}
        weather_key = ['Vehicle_limit_operation',# 限行 限行尾号：1和6
                    'air_temperature',# 气温 6
                    'weather',# 天气 晴
                    'air_quality',# 空气质量 空气质量 良
                    'wind_power',# 风力 北风 2级
                    'humidity',# 湿度 湿度：37%
                    'ultraviolet_rays',# 紫外线 紫外线：4级
                    'pressure',# 气压 气压1015百帕
                    'body_sensation',# 体感 凉
                    'Somatosensory_temperature',# 体感温度 10℃
                    'visibility',# 能见度 良好
                    'visibility_distance',# 能见距离 9.9km
                    'cloudiness',# 云量 晴
                    'cloud_ratio',# 云量比 7%
                    'sunrise_time',# 日出时间 日出：07:23
                    'sunset_time',# 日落时间 日落：17:56
                    ]
        weather_xpath = ['//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[1]/span/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[2]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[1]/span/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/span[1]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[3]/div[1]/span[2]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/span[1]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/span[2]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/span[3]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[1]/p/span[2]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[1]/div/div[1]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[2]/p/span[2]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[2]/div/div[1]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[3]/p/span[2]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[3]/div/div[1]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[3]/div[2]/p[2]/span[1]/text()',
                        '//*[@id="china-weather"]/div[2]/div[2]/div[3]/div[2]/p[2]/span[2]/text()']
        for i in range(len(weather_key)):
            if i == 1:
                weather[weather_key[i]] = s.xpath(weather_xpath[i])[0]+'℃'
            else:
                weather[weather_key[i]] = s.xpath(weather_xpath[i])[0]
        data['weather'] = weather

        air_quality = {}
        air_quality_key = ['air_quality',# 空气质量 良
                        'air_quality_recommendations',# 空气质量建议 空气良好，可以正常参加户外活动。
                        'air_quality_recommendations_list',# 空气质量建议列表 ['无需戴口罩', '适宜外出', '适宜开窗', '关闭净化器']
                        'pollutant_index_list',# 污染物指数列表 0:Pm2.5, 1:pm10, 2:O3, 3:NO2 4:SO2 ['54', '65', '88', '15', '9']
                        ]
        air_quality_xpath = ['//*[@id="quality-chart-0"]/div[1]/div/p/text()',
                            '//*[@id="quality-chart-0"]/div[2]/text()',
                            '//*[@id="quality-detail-0"]/div[1]/div[2]/div/p/text()',
                            '//*[@id="quality-detail-0"]/div[2]/div/div/div/p[2]/span[1]/text()']
        for i in range(len(air_quality_key)):
            if i > 1:
                air_quality[air_quality_key[i]] = s.xpath(air_quality_xpath[i])
            else:
                air_quality[air_quality_key[i]] = s.xpath(air_quality_xpath[i])[0]
        data['air_quality'] = air_quality
        return data

    def week_weather(self):
        url = 'http://pc.weathercn.com/weather/week/'+self.cityCode+'/?partner=&p_source=&p_type=jump'
        res = requests.get(url = url)
        print(res)
        html = res.text
        s = etree.HTML(html)

        data = []
        week_weather = {}
        week_weather_key = ['date',# 明天(02-05)
                        'weather',# 天气 晴
                        'air_temperature',# 气温 6
                        'air_quality',# 空气质量 良
                        'wind_power'# 风力 北风 2级
                        ]
        for n in range(1,8):
            week_weather_xpath = '//*[@id="china-weather"]/div[2]/div[2]/div[2]/div[2]/div/a['+str(n)+']/p/text()'
            week_weather_list = s.xpath(week_weather_xpath)
            for i in range(len(week_weather_list)):
                if week_weather_list[i] == "— —":
                    week_weather[week_weather_key[i]] = "暂无"
                else:
                    week_weather[week_weather_key[i]] = week_weather_list[i]
            data.append(week_weather)
            week_weather = {}
        return data

    def hours_weather(self):
        url = 'http://pc.weathercn.com/weather/week/'+self.cityCode+'/?partner=&p_source=&p_type=jump'
        res = requests.get(url = url)
        print(res)
        html = res.text
        s = etree.HTML(html)

        data = []
        hours_weather = {}
        hours_weather_key = ['time',
                            'weather',
                            'air_quality']

        for n in range(1,72):
            hours_weather_xpath = '//*[@id="weather-72forecast"]/div[2]/div[1]/div['+str(n)+']/p/text()'
            hours_weather_list = s.xpath(hours_weather_xpath)
            for i in range(len(hours_weather_list)):
                hours_weather[hours_weather_key[i]] = hours_weather_list[i]
            data.append(hours_weather)
            hours_weather = {}
        return data

    def weather_suggestion(self):
        url = 'http://pc.weathercn.com/weather/week/'+str(self.cityCode)+'/?partner=&p_source=&p_type=jump'
        res = requests.get(url = url)
        print(res)
        html = res.text
        s = etree.HTML(html)

        data = {}
        data_key = ['sport',
                    'travel',
                'health']
        for types in range(1,4):
            temp = {}
            for n in range(1,6):
                xpath = '//*[@id="china-weather"]/div[5]/div[2]/div/div[3]/div/div['+str(types)+']/div/svg/g/g['+str(n)+']/text/text()'
                text_list = s.xpath(xpath)
                print(text_list)
                temp[text_list[0]] = text_list[1]
            data[data_key[types-1]] = temp

        '//*[@id="china-weather"]/div[5]/div[2]/div/div[3]/div/div[2]/div/svg/g/g[1]/text[1]'
        return data

if __name__ == '__main__':
    w = weather("郑州")
    print(w.real_time_weather())
    print(w.week_weather())
    print(w.hours_weather())
    print(w.weather_suggestion())
