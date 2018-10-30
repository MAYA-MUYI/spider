import requests
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"


def get_data(list, html):
    tables = BeautifulSoup(html, 'html.parser').find('div', {'class': 'indent'}).find_all('table')
    for table in tables:
        title = table.find('div', {'class': 'pl2'}).find('a').get_text()
        info = table.find('p', {'class': 'pl'}).get_text()
        list.append([title.strip(), info.strip()])


def print_data(list):
    print("{:^6}\t{:^10}\t{:^16}".format('序号', '书名', '信息'))
    count = 0
    for b in list:
        count += 1
        print("{:^6}\t{:^16}\t{:^16}".format(count, b[0], b[1]))


def main():
    start_url = 'https://book.douban.com/top250?'
    depth = 10
    info_list = []
    for i in range(depth):
        url = start_url + str(25 * i)
        html = getHTMLText(url)
        get_data(info_list, html)
    print_data(info_list)


if __name__ == '__main__':
    main()
