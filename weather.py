import requests
from bs4 import BeautifulSoup


def parse_page(url):
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"

    }
    req = requests.get(url, headers= headers)
    text = req.content.decode('utf-8')
    soup = BeautifulSoup(text, 'xml')
    conMidtab = soup.find("div", attrs={'class':'conMidtab'})
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):

            tds = tr.find_all('td')
            city_td = tds[0]
            if index ==0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            temp = list(temp_td.stripped_strings)[0]
            # print("city:"+city+"min_temp:"+temp)
            print({"city":city, "min_temp":temp+"度"})



def main():
    urls = [


        "http://www.weather.com.cn/textFC/hb.shtml",
        "http://www.weather.com.cn/textFC/db.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/hd.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        "http://www.weather.com.cn/textFC/gat.shtml"
    ]
    for url in urls:
        parse_page(url)




if __name__ == '__main__':
    main()
