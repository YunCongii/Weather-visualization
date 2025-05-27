import requests
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import matplotlib

# ===== 0. 环境配置 =====
# 设置中文字体（Windows系统）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 微软雅黑
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ===== 1. 配置参数 =====
API_KEY = "weatherapi"  # 替换为实际Key
CITY_NAME = "ZhengZhou"  # 支持城市名/经纬度/IP


# ===== 2. 数据获取 =====
def get_weather_forecast():
    """获取7天天气预报数据（带错误处理）"""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={CITY_NAME}&days=7&aqi=no&alerts=no"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if "error" not in data:
            return {
                "location": data["location"]["name"],
                "forecast": data["forecast"]["forecastday"],
                "current": data["current"]
            }
        else:
            print(f"API错误: {data['error']['message']}")
            return None
    except Exception as e:
        print(f"数据获取失败: {str(e)}")
        return None


# ===== 3. 独立图表生成函数 =====
def parse_time(time_str):
    """转换 '05:50 AM' 为小时数"""
    try:
        time_part, period = time_str.split()
        hh, mm = map(int, time_part.split(':'))
        if period == 'PM' and hh != 12:
            hh += 12
        elif period == 'AM' and hh == 12:
            hh = 0
        return hh + mm / 60
    except:
        print(f"时间格式错误: {time_str}")
        return 0


def generate_temperature_chart(forecast, location):
    """生成温度曲线图"""
    dates = [datetime.strptime(day['date'], "%Y-%m-%d").strftime("%m-%d") for day in forecast]
    max_temps = [day['day']['maxtemp_c'] for day in forecast]
    min_temps = [day['day']['mintemp_c'] for day in forecast]

    plt.figure(figsize=(10, 5), facecolor='#F5F5F5')
    plt.plot(dates, max_temps, 'o-', color='#FF6B6B', label='最高气温', linewidth=2)
    plt.plot(dates, min_temps, 'o-', color='#4D96FF', label='最低气温', linewidth=2)
    plt.fill_between(dates, max_temps, min_temps, color='#FFD93D', alpha=0.15)

    # 添加数据标签
    for i, (d, mx, mn) in enumerate(zip(dates, max_temps, min_temps)):
        plt.text(i, mx + 0.5, f'{mx}°C', ha='center', va='bottom', fontsize=9)
        plt.text(i, mn - 0.5, f'{mn}°C', ha='center', va='top', fontsize=9)

    plt.title(f'{location} 7天温度变化', fontsize=14)
    plt.ylabel('温度 (°C)')
    plt.legend()
    plt.grid(linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('temperature.png', dpi=120)
    plt.close()


def generate_weather_pie(forecast, location):
    """生成天气状况饼图"""
    weather_conditions = {}
    for day in forecast:
        cond = day['day']['condition']['text']
        weather_conditions[cond] = weather_conditions.get(cond, 0) + 1

    plt.figure(figsize=(8, 6), facecolor='#F5F5F5')
    plt.pie(
        weather_conditions.values(),
        labels=weather_conditions.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Pastel1.colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 0.5}
    )
    plt.title(f'{location} 天气类型分布', fontsize=14)
    plt.tight_layout()
    plt.savefig('weather_conditions.png', dpi=120)
    plt.close()


def generate_humidity_rain_chart(forecast, location):
    """生成湿度与降雨概率图"""
    dates = [datetime.strptime(day['date'], "%Y-%m-%d").strftime("%m-%d") for day in forecast]
    humidity = [day['day']['avghumidity'] for day in forecast]
    rain_chance = [day['day']['daily_chance_of_rain'] for day in forecast]

    plt.figure(figsize=(10, 5), facecolor='#F5F5F5')
    ax = plt.gca()
    ax2 = ax.twinx()

    l1, = ax.plot(dates, humidity, 's-', color='#6BCB77', label='湿度 (%)', linewidth=2)
    l2, = ax2.plot(dates, rain_chance, 'd-', color='#4D96FF', label='降雨概率 (%)', linewidth=2)

    ax.set_ylabel('湿度 (%)')
    ax2.set_ylabel('降雨概率 (%)')
    ax.legend(handles=[l1, l2], loc='upper left')
    plt.title(f'{location} 湿度与降雨概率', fontsize=14)
    ax.grid(linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('humidity_rain.png', dpi=120)
    plt.close()


def generate_wind_chart(forecast, location):
    """生成风速雷达图"""
    dates = [datetime.strptime(day['date'], "%Y-%m-%d").strftime("%m-%d") for day in forecast]
    wind_speeds = [day['day']['maxwind_kph'] for day in forecast]
    angles = np.linspace(0, 2 * np.pi, len(dates), endpoint=False).tolist()
    angles += angles[:1]
    wind_speeds += wind_speeds[:1]

    plt.figure(figsize=(8, 6), facecolor='#F5F5F5')
    ax = plt.subplot(111, polar=True)
    ax.plot(angles, wind_speeds, 'o-', linewidth=2, color='#845EC2')
    ax.fill(angles, wind_speeds, color='#845EC2', alpha=0.15)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dates)
    ax.set_title(f'{location} 风速变化 (km/h)', fontsize=14)
    plt.tight_layout()
    plt.savefig('wind_speed.png', dpi=120)
    plt.close()


def generate_sun_chart(forecast, location):
    """生成日出日落时间图"""
    dates = [datetime.strptime(day['date'], "%Y-%m-%d").strftime("%m-%d") for day in forecast]
    sun_data = {
        '日出': [day['astro']['sunrise'] for day in forecast],
        '日落': [day['astro']['sunset'] for day in forecast]
    }

    plt.figure(figsize=(10, 5), facecolor='#F5F5F5')
    width = 0.35
    x = np.arange(len(dates))

    for i, (label, times) in enumerate(sun_data.items()):
        hours = [parse_time(t) for t in times]
        plt.bar(x + width * i, hours, width, label=label,
                color=['#FFC154', '#47B39C'][i], edgecolor='white')

    plt.xticks(x + width / 2, dates)
    plt.yticks([4, 6, 8, 10, 12, 14, 16, 18, 20],
               ["4:00", "6:00", "8:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"])
    plt.title(f'{location} 日出日落时间', fontsize=14)
    plt.legend()
    plt.grid(True, axis='y', linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig('sunrise_sunset.png', dpi=120)
    plt.close()


# ===== 4. 主程序 =====
if __name__ == "__main__":
    print("⏳ 正在获取天气数据...")
    weather_data = get_weather_forecast()

    if weather_data:
        # 打印当前天气
        current = weather_data['current']
        print("\n=== 当前天气 ===")
        print(
            f"📍 位置: {weather_data['location']}\n"
            f"🌡️ 温度: {current['temp_c']}°C (体感 {current['feelslike_c']}°C)\n"
            f"🌤️ 天气: {current['condition']['text']}\n"
            f"💧 湿度: {current['humidity']}% | 🌬️ 风速: {current['wind_kph']} km/h {current['wind_dir']}"
        )

        # 打印预报
        print("\n=== 7天预报 ===")
        for day in weather_data['forecast']:
            print(
                f"{day['date']}: {day['day']['condition']['text']} | "
                f"🌡️ {day['day']['mintemp_c']}~{day['day']['maxtemp_c']}°C | "
                f"💧 湿度 {day['day']['avghumidity']}% | "
                f"🌧️ 降雨 {day['day']['daily_chance_of_rain']}%"
            )

        # 生成独立图表
        print("\n🖌️ 正在生成可视化图表...")
        forecast = weather_data['forecast']
        location = weather_data['location']

        generate_temperature_chart(forecast, location)
        generate_weather_pie(forecast, location)
        generate_humidity_rain_chart(forecast, location)
        generate_wind_chart(forecast, location)
        generate_sun_chart(forecast, location)

        print("✔ 所有图表已保存为独立图片：")
        print(
            "- temperature.png\n- weather_conditions.png\n- humidity_rain.png\n- wind_speed.png\n- sunrise_sunset.png")
    else:
        print("❌ 获取天气数据失败，请检查API Key和网络连接")