import requests
from bs4 import BeautifulSoup
import json
import codecs

def GetHtmlText(url):
    try:
        headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36"} #随机构造请求头，增加一定的反反爬能力。
        r = requests.get(url, timeout=5, headers=headers)
        r.raise_for_status() #判断r若果不是200，产生异常requests.HTTPError异常
        r.encoding = r.apparent_encoding
        return r.text  #http响应内容的字符串形式，即URL返回的页面内容
    except:
        return None

def fillJobList(html):
    soup = BeautifulSoup(html,'html.parser') #解析网页源代码
    dic = {}
    test_list = []
    for job in soup.findAll('div',{'class':'info-primary'}):
        try:
            position = job.find('div',{'class':'job-title'}).text
            pay = job.find('span',{'class':'red'}).text
            edu = job.find('p').text
            dic['position'] = position
            dic['pay'] = pay
            dic['edu'] = edu
            detail_url = job.find('a').attrs['href']
            detail_html = GetHtmlText('https://www.zhipin.com'+ detail_url)
            detail_soup = BeautifulSoup(detail_html, 'html.parser')
            detail = detail_soup.find('div', {'class': 'text'}).text.strip()
            dic['detail'] = detail
            # print(dic)
            test_list.append(dic)
        except:
            continue
    return test_list

def write(dic):

    with open("data.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(dic, ensure_ascii=False))
    # with open('jobs.json', 'w', encoding='utf-8') as f:
    #     fp = json.dumps(dic,  ensure_ascii=False)
    #     f.write(fp)

def main():
    keywords = input('输入职位:')
    pages = int(input('获取页数:'))
    for i in range(1, pages + 1):
        url = 'https://www.zhipin.com/c101270100-p100109/?query=' + keywords + '&page=' + str(i)
        html = GetHtmlText(url)
        print(fillJobList(html))
        print(len(fillJobList(html)))
        #for i in fillJobList(html):
        #     write(i)



if __name__ == '__main__':
    main()