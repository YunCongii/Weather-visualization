使用weather api获取天气数据，免费版为100万次/月  
weather api地址 https://www.weatherapi.com/

核心库使用
| 库名称     	| 用途                                 	| 安装命令               	|
|------------	|--------------------------------------	|------------------------	|
| requests   	| 发送HTTP请求获取天气API数据           	| pip install requests   	|
| matplotlib 	| 生成所有可视化图表（折线图、饼图等）   	| pip install matplotlib 	|
| numpy      	| 数值计算（处理雷达图坐标等）            	| pip install numpy      	|
| datetime   	| 处理日期时间格式转换                  	| Python内置，无需安装   	|

Matplotlib相关子模块
| 模块         	| 用途                       	|
|--------------	|----------------------------	|
| pyplot (plt) 	| 基础绘图接口               	|
| gridspec     	| 创建复杂的图表布局         	  |
| rcParams     	| 设置全局样式（如中文字体）   	|
| cm           	| 颜色映射（饼图配色）         	|

关键功能对应库  
1.数据获取  
requests.get()：从WeatherAPI获取JSON数据
2.可视化  
plt.plot()：温度曲线  
plt.pie()：天气分布饼图  
plt.bar()：日出日落时间柱状图  
polar plot：风速雷达图  
twinx()：双Y轴湿度/降雨曲线  
3.数据处理  
numpy.linspace()：生成雷达图角度  
datetime.strptime()：解析日期字符串  

验证库安装  
import requests, matplotlib, numpy  
print(  
    f"requests版本: {requests.__version__}\n"  
    f"matplotlib版本: {matplotlib.__version__}\n"  
    f"numpy版本: {numpy.__version__}"  
)  

运行代码  
替换 API_KEY 为WeatherAPI Key  
可修改 CITY_NAME 为其他城市  
