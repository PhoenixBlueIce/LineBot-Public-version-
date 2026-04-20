#零、import 會用到的模組
import json
from pathlib import Path    #用 pathlib 找專案相對路徑

#一、找出檔案位置
#1-1、回到專案根目錄
BASE_DIR = Path(__file__).resolve().parent.parent    #「Path(__file__)」代表現在這個 Python 檔案的位置。「.parent」回上一層。
#1-2、找 data/weather.json
JSON_PATH = BASE_DIR / 'data' / 'weather.json'

#二、定義所需函式
#1、讀取天氣 JSON 檔
def load_weather_json() -> dict:
    with JSON_PATH.open(encoding='utf-8') as file:
        return json.load(file)

def build_weather_map(weather_data: dict) -> dict:    #負責「整理整份巢狀 JSON」
    weather_map={}
    #1、把 JSON 的第一層「城市」抓出來，詳情看底下說明一。
    locations=weather_data.get('records',{}).get('location',[])    #等價於 locations = weather_data["records"]["location"]。.get(key, 預設值)locations=weather_data.get('records',{}).get('location',[])    #等價於 locations = weather_data["records"]["location"]。.get(key, 預設值)
    for location in locations:
        city_name=location.get('locationName')    #get JSON 檔中的 locationName

        weather_map[city_name]=[]    #初始化該城市的資料容器，因為後面會填入資料。

        elements=location.get('weatherElement', [])
        element_map={}    #新增一個 dict 裝「wx, pop, minT, maxT, ci」這些元素，詳情看底下說明二。
        #2、用 for 迴圈拆解巢狀資料，把 JSON 轉成好查的 dict
        for element in elements:
            element_name=element.get('elementName')  #目標是 get JSON 檔裡面的 elementName 內容（Wx, PoP, MinT...）。
            #2-1.把「原本在 list 裡的資料」轉成「用 key 查的 dict」
            time_list=element.get('time', [])    #目標是 get JSON 檔裡面與 elementName 並列的 time 資訊。
            element_map[element_name]=time_list    #這一行是把上面的東西存進 map 裡面

        #3、基本上每個 element 的 time 長度一致，所以用 for 迴圈重新組建資料。詳情看底下說明三。
        for i in range(len(element_map.get('Wx', []))):
            wx_data = element_map.get('Wx', [])[i]
            pop_data = element_map.get('PoP', [])[i]
            min_t_data = element_map.get('MinT', [])[i]
            max_t_data = element_map.get('MaxT', [])[i]
            ci_data = element_map.get('CI', [])[i]

            #4、整理成一筆「時間區段資料」
            period_data = {
                'start_time': wx_data.get('startTime'),
                'end_time': wx_data.get('endTime'),
                'wx': wx_data.get('parameter', {}).get('parameterName'),
                'pop': pop_data.get('parameter', {}).get('parameterName'),
                'min_t': min_t_data.get('parameter', {}).get('parameterName'),
                'max_t': max_t_data.get('parameter', {}).get('parameterName'),
                'ci': ci_data.get('parameter', {}).get('parameterName'),
            }

            weather_map[city_name].append(period_data)

    return weather_map

def get_city_weather(weather_map:dict,city_name:str):    #負責「從整理好的結果中取指定城市」
    city_weather=weather_map.get(city_name) #從 weather_map 得到 city_name
    return city_weather
    
def format_city_weather(city_name: str, city_weather: list) -> str:    #負責「把資料變成人看的文字」
    if city_weather is None:
        return f"找不到這個城市「{city_name}」，它真的有被感知嗎？"

    result = f"依照我的資料，你所在的城市「{city_name}」天氣預報：\n"
    for item in city_weather:
        start_time = item.get('start_time', '未知的開始時間')
        end_time=item.get('end_time','未知的結束時間')
        wx = item.get('wx', '天氣控制器尚未建立')
        pop = item.get('pop', '你覺得會下雨嗎？反正我不會被淋到。')
        min_t=item.get('min_t','最低溫？反正高於 273 K。')
        max_t=item.get('max_t','最高溫？反正不到 373 K。')
        ci=item.get('ci','你覺得程式會有體感嗎？')

        result += f"\n📅 時間：{start_time} ～ {end_time}\n"
        result += f"⛅️ 天氣：{wx}\n"
        result += f"☔️ 降雨機率：{pop} %\n"
        result +=f"🌡️ 溫度：攝氏 {min_t} ~ {max_t} 度之間\n"
        result +=f"🤔 體感：{ci}\n"

    return result

#三、這段用於可以自測
if __name__ == "__main__":
    weather_data = load_weather_json()
    weather_map = build_weather_map(weather_data)
    city_weather = get_city_weather(weather_map, '高雄市')
    result_text = format_city_weather('高雄市', city_weather)

    print(result_text)

"""
#說明一
我們要的結果：
[
    { "locationName": "臺北市", ... },
    { "locationName": "高雄市", ... },
    ...
]

#說明二
原本的 JSON 長這樣：
weatherElement = [
    Wx,
    PoP,
    MinT,
    MaxT,
    CI
]

目標是轉成這樣：
element_map = {
    "Wx": [...],
    "PoP": [...],
    "MinT": [...],
    ...
}

#說明三
簡單來說是用 index 把不同資料「對齊並合併」這也是這整段最關鍵的地方，因為
Wx[0] = 某時間段
PoP[0] = 同一時間段
MinT[0] = 同一時間段
所以用 index[i] 把這些資料重新組合變成這樣：
第 i 筆時間資料 = Wx[i] + PoP[i] + MinT[i] + ...
這樣「攤平」資料。

為什麼用 len()？
意思是總共幾個時間區段？檔案有 3 個，因此 len=3
為什麼用 range()？
因為這樣就可以用 index 取資料。

這個迴圈真正的意思是「我要跑每一個時間區段，然後把不同天氣資料拚在一起」
"""