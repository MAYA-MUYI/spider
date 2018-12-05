import requests
from bs4 import BeautifulSoup
import time
import json


def get_page():
    headers = {
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Host': 'www.lagou.com',
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Referer': "https://www.lagou.com/jobs/list_python?city=%E5%8C%97%E4%BA%AC&cl=false&fromSearch=true&labelWords=&suginput=",
        'Cookie': "_ga=GA1.2.910872852.1537274650; _gid=GA1.2.551069079.1537274650; user_trace_token=20180918204408-89394348-bb40-11e8-a1fb-525400f775ce;"
                " LGUID=20180918204408-89394691-bb40-11e8-a1fb-525400f775ce; index_location_city=%E5%8C%97%E4%BA%AC; "
                "JSESSIONID=ABAAABAAADEAAFI9B8A5B922B0F62DE98F3D76FFB498FD3; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537274650,1537343453;"
                " LGSID=20180919155053-bbaaf688-bbe0-11e8-baf2-5254005c3644; "
                "PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_python%3FlabelWords%3D%26fromSearch%3Dtrue%26suginput%3D; "
                "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1537343456; LGRID=20180919155055-bd698539-bbe0-11e8-a233-525400f775ce; TG-TRACK-CODE=search_code;"
                " SEARCH_ID=d8d49e5d780449e4adf77e35cbf240a9",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'X-Anit-Forge-Code': "0",
        'X-Anit-Forge-Token': None,
        'X-Requested-With': 'XMLHttpRequest'

    }

    positions = []
    for x in range(1,31):
        form_data = {
            'first': 'false',
            'pn': x,
            'kd': 'python'
        }

        response = requests.post("https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false", headers=headers, data=form_data)

        json_result = response.json()
        page_positions = json_result['content']['positionResult']['result']
        #extend方法可以把一个列表添加到另一个列表
        positions.extend(page_positions)
        time.sleep(3)
        print("*************************")
        print(page_positions)


def main():
    get_page()

if __name__ == '__main__':
    main()