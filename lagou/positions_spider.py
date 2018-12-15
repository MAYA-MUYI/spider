#!/usr/bin/python
#-*-coding:utf-8 -*-
import requests
# from bs4 import BeautifulSoup
import time
import pymysql
import json
import codecs
import io


def get_page():
    #构造头信息
    headers = {
        'Accept-Language': "zh-CN,zh;q=0.9",
        'Host': 'www.lagou.com',
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36",
        'Referer': "https://www.lagou.com/jobs/list_python?city=%E5%85%A8%E5%9B%BD&cl=false&fromSearch=true&labelWords=&suginput=",
        'Cookie': "user_trace_token=20181205153237-2fb5c5de-ddba-45ae-a4e5-1d3f994363da; _ga=GA1.2.1973907981.1543995170; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221677d489b4c51b-01ad0f1ff9cf7e-7d113749-1049088-1677d489b4e157%22%2C%22%24device_id%22%3A%221677d489b4c51b-01ad0f1ff9cf7e-7d113749-1049088-1677d489b4e157%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; LGUID=20181205153247-f6746e6e-f85f-11e8-8ce2-5254005c3644; index_location_city=%E5%85%A8%E5%9B%BD; _gid=GA1.2.498204391.1544690905; JSESSIONID=ABAAABAAAGGABCB41C4F7888779A017173A237D896F7D51; TG-TRACK-CODE=index_search; _putrc=D253F09634921DCE123F89F2B170EADC; login=true; unick=%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B73051; hasDeliver=0; PRE_UTM=; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544699176,1544759671,1544762963,1544767071; LGSID=20181214135750-304386ec-ff65-11e8-918d-525400f775ce; PRE_HOST=www.google.com; PRE_SITE=https%3A%2F%2Fwww.google.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; gate_login_token=be2fd084aa6ff0923a8d24de7aace358683b2c405e52960c9220540a0c9f3693; LGRID=20181214141147-23a73cc0-ff67-11e8-918d-525400f775ce; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1544767909; SEARCH_ID=57101ec6359e40efad24074934907963",
        'Accept': "application/json, text/javascript, */*; q=0.01",
        'X-Anit-Forge-Code': "0",
        'X-Anit-Forge-Token': None,
        'X-Requested-With': 'XMLHttpRequest'

    }
    #翻页构造
    for x in range(26, 31):
        form_data = {
            'first': 'false',
            'pn': x,
            'kd': 'python'
        }
        print("正在解析第%s页" %form_data['pn'])
        #post请求
        response = requests.post("https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false", headers=headers, data=form_data)
        position = []
        #直接获取json格式的数据
        json_result = response.json()
        print(json_result)
        #一层一层的获取到需要的数据
        page_positions = json_result['content']['positionResult']['result']
        time.sleep(10)
        result = []
        for position in page_positions:
            #返回数据字典
            position_dict = {
                'position_name': position['positionName'],
                'work_year': position['workYear'],
                'salary': position['salary'],
                'district': position['district'],
                'company_name': position['companyFullName'],
                'companySize': position['companySize'],
                'positionAdvantage': position['positionAdvantage']
            }
            # print(position_dict)
            #写入json文件
            f = codecs.open('positions.json', 'a', 'utf-8')
            f.write(json.dumps(position_dict, ensure_ascii=False)+"\n")
            f.close()
            # return json.dumps(position_dict, ensure_ascii=False)



def create_table():
    conn = pymysql.connect(db='test', user='root', passwd='299521', host='localhost')
    cursor = conn.cursor()
    # create a table
    cursor.execute("drop table if exists position")
    sql = """create table position (
                id int not null auto_increment primary key,
                position_name varchar(20) not null character set utf8mb4 COLLATE utf8mb4_general_ci,
                work_year varchar(20) not null character set utf8mb4 COLLATE utf8mb4_general_ci,
                salary varchar(20) not null character set utf8mb4 COLLATE utf8mb4_general_ci,
                district varchar(20) not null character set utf8mb4 COLLATE utf8mb4_general_ci,
                company_name varchar(20) not null character set utf8mb4 COLLATE utf8mb4_general_ci,
                companySize varchar(20) not null character set utf8mb4 COLLATE utf8mb4_general_ci,
                positionAdvantage varchar(40) not null character set utf8mb4 COLLATE utf8mb4_general_ci)character set utf8mb4 COLLATE utf8mb4_general_ci"""

    cursor.execute(sql)

def insert():
    conn = pymysql.connect(db='test', user='root', passwd='299521', host='localhost')
    cursor = conn.cursor()

    with open('positions.json', 'r', encoding='utf-8') as f:
        i = 0
        for lines in f.readlines():
            i += 1
            print('正在载入第%s行......' % i)
            try:
                # lines = f.readline()  # 使用逐行读取的方法
                review_text = json.loads(lines, encoding='utf-8')  # 解析每一行数据
                result = []
                result.append((review_text['salary'], review_text['companySize'], review_text['district'],
                               review_text['work_year'], review_text['company_name'], review_text['position_name'],
                               review_text['positionAdvantage']))
                print(result)

                inesrt_re = "insert into position (salary, companySize, district, work_year, company_name, position_name,positionAdvantage) values (%s, %s, %s, %s,%s, %s,%s)"
                cursor.executemany(inesrt_re, result)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(str(e))
                break



def main():
    get_page()
    create_table()
    insert()
if __name__ == '__main__':
    main()