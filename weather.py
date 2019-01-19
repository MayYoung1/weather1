"""
Created by Young on 2019/1/18 17:37
"""

import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

urls = {
'http://www.weather.com.cn/textFC/hb.shtml',
'http://www.weather.com.cn/textFC/db.shtml',
'http://www.weather.com.cn/textFC/hd.shtml',
'http://www.weather.com.cn/textFC/hz.shtml',
'http://www.weather.com.cn/textFC/hn.shtml',
'http://www.weather.com.cn/textFC/xb.shtml',
'http://www.weather.com.cn/textFC/xn.shtml',
'http://www.weather.com.cn/textFC/gat.shtml',
}
ALL_DATA = []
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}

def getHTMLText(url):
    try:
        wb_data = requests.get(url, timeout=30, headers=headers)
        wb_data.encoding = "utf-8"  # 解决乱码
        soup = BeautifulSoup(wb_data.text, 'html5lib', from_encoding="utf8")
        conMidtab = soup.find('div',class_='conMidtab')
        tables = conMidtab.find_all('table')
        for table in tables:
            trs = table.find_all('tr')[2:]
            for index,tr in enumerate(trs):
                tds = tr.find_all('td')
                city_td = tds[0]
                if index == 0:
                    city_td = tds[1]
                city = list(city_td.stripped_strings)[0]
                temp_td = tds[-2]
                min_temp = list(temp_td.stripped_strings)[0]
                ALL_DATA.append({"city":city,"min_temp":int(min_temp)})
                print(({"city":city,"min_temp":int(min_temp)}))

    except:
        return '产生异常'


def main():
    for url in urls:
        getHTMLText(url)
    ALL_DATA.sort(key = lambda x:x['min_temp'])
    data = ALL_DATA[0:10]
    cites = list(map(lambda x:x['city'],data))
    temps = list(map(lambda x:x['min_temp'],data))
    chart = Bar("中国天气最低气温排行榜")
    chart.add('',cites,temps)
    chart.render('weather.html')

if __name__ == '__main__':
    main()
