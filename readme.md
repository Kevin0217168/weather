# python天气信息获取模块
 #### &#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;基于lxml，requests，bs4库。爬取中国天气网
### 使用前必看
使用的库有 lxml，requests，json，pickle，bs4，re，os
>其中*lxml*，*requests*，*bs4*库 python不自带，需要自行检查并安装
以下提供pip的下载方法，由于国内pip下载过慢，此处将使用清华镜像源下载
如果仍然发生超时(time out)请再尝试一次
```python
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ lxml

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ requests

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ bs4
```
### 使用方法
 #### 导入库
```python
import weather
```

>此模块方法封装在**weather**类中，在调用方法前需要先实例化此类
需传入要查找的城市名称
要注意：不支持县，村级，不支持直接输入省名，国外城市，可查询省内城市及直辖市

可行的方法
```python
w = weather("郑州")
```
不支持的方法
```python
# 查找了县级
w = weather("通许")
Exception: 查找不到该城市

# 查找了省名
w = weather("河南")
Exception: 不支持查找整个省的天气，可尝试查找省会郑州，或省内其他城市

# 查找了国外城市
w = weather("堪培拉")
Exception: 查找不到该城市
```

 #### 内部方法概要
方法|用途|参数|返回值
-|:-|:-|:-
real_time_weather|获取实时天气信息|无|python字典
weather_suggestion|获取实时天气建议|无|python字典
week_weather|获取14天天气信息|无|python列表
hours_weather|获取72小时天气信息|无|python列表

 #### real_time_weather获取实时天气信息方法
  ##### 返回值信息(字典dict)
字典键|键|注解|示例值|类型
:-|:-|:-|:-|-
date|Huang_Li|黄历列表|宜/忌|列表(list)
||week|星期|星期一|字符串(str)
||lunar_calendar|农历|农历正月初十|
weather|Vehicle_limit_operation |限行尾号|限行尾号：1和6|
||air_temperature|气温|6|
||weather|天气|晴|
||air_quality|空气质量|空气质量 良|
||wind_power|风力|北风 2级|
||humidity|湿度|湿度：37%|
||ultraviolet_rays|紫外线|紫外线：4级|
||pressure|气压|气压1015百帕|
||body_sensation|体感|凉|
||Somatosensory_temperature|体感温度|10℃|
||visibility|能见度|良好|
||visibility_distance|能见距离|9.9km|
||cloudiness|云量|晴|
||cloud_ratio|云量比|7%|
||sunrise_time|日出时间|日出：07:23|
||sunset_time|日落时间|日落：17:56|
air_quality|air_quality|空气质量|良|
||air_quality_recommendations|空气质量建议|空气良好，可以正常参加户外活动。|
||air_quality_recommendations_list|空气质量建议列表|['无需戴口罩', '适宜外出', '适宜开窗', '关闭净化器']|列表(list)
||pollutant_index_list|污染物指数列表0:Pm2.5, 1:pm10, 2:O3, 3:NO2 4:SO2|['54', '65', '88', '15', '9']|
  ##### 程序示例
```python
w.weather("郑州")
weather_dict = w.real_time_weather()
```
  ##### 返回示例
```json
{
    "date": {
        "Huang_Li": [
            "宜: 祭祀、祈福、求嗣、斋醮、入殓、除服、成服、移柩、安葬、启钻",
            "忌: 嫁娶、动土、开光、盖屋、破土"
        ],
        "week": "星期二",
        "lunar_calendar": "农历正月十一"
    },
    "weather": {
        "Vehicle_limit_operation": "限行尾号：2和7",
        "air_temperature": "8℃",
        "weather": "霾",
        "air_quality": "空气质量 轻度污染",
        "wind_power": "东风 2级",
        "humidity": "湿度：51%",
        "ultraviolet_rays": "紫外线：3级",
        "pressure": "气压1011百帕",
        "body_sensation": "凉",
        "Somatosensory_temperature": "10℃",
        "visibility": "中等",
        "visibility_distance": "4.4km",
        "cloudiness": "多云",
        "cloud_ratio": "51%",
        "sunrise_time": "日出：07:22",
        "sunset_time": "日落：17:57"
    },
    "air_quality": {
        "air_quality": "轻度污染",
        "air_quality_recommendations": "空气一般，敏感人员外出时，需做好防护措施。",
        "air_quality_recommendations_list": [
            "建议戴口罩",
            "减少外出",
            "减少开窗",
            "开启净化器"
        ],
        "pollutant_index_list": [
            "114",
            "112",
            "58",
            "32",
            "13",
            "1"
        ]
    }
}
```

 #### week_weather获取14天天气信息方法
  ##### 返回值信息(列表list)
索引|键|注解|示例值|类型
-|:-|:-|:-|:-
0|date|日期|今天(02-04)|字符串(str)
||weather|天气|晴|
||air_temperature|气温|-1/10℃|
||air_quality|空气质量|良|
||wind_power|风力|北风 2级|
1~13|...同上|...|...|...
>注意：在第8~14天中无法获取空气质量信息，值为"暂无"为正常现象

  ##### 程序示例
```python
w.weather("郑州")
weather_list = w.week_weather()
```
  ##### 返回示例
```json
[
    {
        "date": "今天(02-04)",
        "weather": "晴转多云",
        "air_temperature": "-1/10℃",
        "air_quality": "轻度",
        "wind_power": "东北风 4级"
    },
    {
        "date": "明天(02-05)",
        "weather": "雨夹雪",
        "air_temperature": "-1/1℃",
        "air_quality": "良",
        "wind_power": "东北风 3级"
    },
    {
        "date": "周四(02-06)",
        "weather": "雨夹雪转多云",
        "air_temperature": "-3/2℃",
        "air_quality": "良",
        "wind_power": "东北风 1级"
    },
    {
        "date": "周五(02-07)",
        "weather": "晴",
        "air_temperature": "-2/10℃",
        "air_quality": "良",
        "wind_power": "西南风 3级"
    },
    {
        "date": "周六(02-08)",
        "weather": "多云",
        "air_temperature": "1/13℃",
        "air_quality": "良",
        "wind_power": "西风 3级"
    },
    {
        "date": "周日(02-09)",
        "weather": "晴转多云",
        "air_temperature": "1/15℃",
        "air_quality": "良",
        "wind_power": "西风 3级"
    },
    {
        "date": "周一(02-10)",
        "weather": "阴",
        "air_temperature": "4/16℃",
        "air_quality": "良",
        "wind_power": "南风 3级"
    },
    {
        "date": "周二(02-11)",
        "weather": "多云",
        "air_temperature": "4/13℃",
        "air_quality": "暂无",
        "wind_power": "西北风 1级"
    },
    {
        "date": "周三(02-12)",
        "weather": "晴",
        "air_temperature": "5/19℃",
        "air_quality": "暂无",
        "wind_power": "西北风 1级"
    },
    {
        "date": "周四(02-13)",
        "weather": "晴",
        "air_temperature": "2/15℃",
        "air_quality": "暂无",
        "wind_power": "东南风 1级"
    },
    {
        "date": "周五(02-14)",
        "weather": "晴转多云",
        "air_temperature": "1/12℃",
        "air_quality": "暂无",
        "wind_power": "东北风 3级"
    },
    {
        "date": "周六(02-15)",
        "weather": "多云",
        "air_temperature": "1/11℃",
        "air_quality": "暂无",
        "wind_power": "东南风 1级"
    },
    {
        "date": "周日(02-16)",
        "weather": "小雨",
        "air_temperature": "2/9℃",
        "air_quality": "暂无",
        "wind_power": "北风 1级"
    },
    {
        "date": "周一(02-17)",
        "weather": "多云转晴",
        "air_temperature": "2/12℃",
        "air_quality": "暂无",
        "wind_power": "东南风 1级"
    }
]
```


 #### hours_weather获取72小时天气信息方法
  ##### 返回值信息(列表list)
索引|键|注解|示例值|类型
-|:-|:-|:-|:-
0|time|时间|14时|字符串(str)
||weather|天气|晴|
||air_quality|空气质量|良|
1~71|...同上|...|...|...
  ##### 程序示例
```python
w.weather("郑州")
weather_list = w.hours_weather()
```
  ##### 返回示例
```json
[
    {
        "time": "14时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "15时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "16时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "17时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "18时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "19时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "20时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "21时",
        "weather": "晴",
        "air_quality": "轻度"
    },
    {
        "time": "22时",
        "weather": "晴",
        "air_quality": "良"
    },
    {
        "time": "23时",
        "weather": "晴",
        "air_quality": "良"
    },
    {
        "time": "00时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "01时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "02时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "03时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "04时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "05时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "06时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "07时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "08时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "09时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "10时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "11时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "12时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "13时",
        "weather": "阴",
        "air_quality": "良"
    },
    {
        "time": "14时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "15时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "16时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "17时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "18时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "19时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "20时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "21时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "22时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "23时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "00时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "01时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "02时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "03时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "04时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "05时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "06时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "07时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "08时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "09时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "10时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "11时",
        "weather": "冰霰",
        "air_quality": "良"
    },
    {
        "time": "12时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "13时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "14时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "15时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "16时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "17时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "18时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "19时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "20时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "21时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "22时",
        "weather": "多云",
        "air_quality": "优"
    },
    {
        "time": "23时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "00时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "01时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "02时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "03时",
        "weather": "多云",
        "air_quality": "良"
    },
    {
        "time": "04时",
        "weather": "大部分多云",
        "air_quality": "良"
    },
    {
        "time": "05时",
        "weather": "间歇性多云",
        "air_quality": "良"
    },
    {
        "time": "06时",
        "weather": "间歇性多云",
        "air_quality": "良"
    },
    {
        "time": "07时",
        "weather": "部分多云",
        "air_quality": "良"
    },
    {
        "time": "08时",
        "weather": "部分晴",
        "air_quality": "良"
    },
    {
        "time": "09时",
        "weather": "部分晴",
        "air_quality": "良"
    },
    {
        "time": "10时",
        "weather": "大部分晴",
        "air_quality": "良"
    },
    {
        "time": "11时",
        "weather": "大部分晴",
        "air_quality": "良"
    },
    {
        "time": "12时",
        "weather": "部分晴",
        "air_quality": "良"
    }
]
```