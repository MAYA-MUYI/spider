import requests
from bs4 import BeautifulSoup
from lxml import etree
import re


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


def get_data(html):
    # tree = etree.HTML(html)
    # trs = tree.xpath('//table[@class="table table-small-font table-bordered table-striped arwu"]/tbody/tr')
    # for tr in trs:
    #     school_name = tr.xpath('./td[2]//text()')[0]
    #     school_index = tr.xpath('./td[1]/text()')[0]
    #     print("学校:%s, 排名:%s" %(school_name, school_index))

    names = re.findall('<a target="_blank" href.*?>(.*?)</a>', html)
    index = re.findall('<tr.*?><td>(.*?)</td>', html)
    # print(index)
    for i,j in zip(range(1, len(names)-3, 2), range(len(index))):
        print("学校：%s  排名: %s" %(names[i-1], index[j]))
        # print(names[i-1])


def main():
    start_url = 'http://zuihaodaxue.cn/ARWU2018.html'
    html = getHTMLText(start_url)
    get_data(html)


if __name__ == '__main__':
    main()