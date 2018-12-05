from lxml import etree
from multiprocessing.dummy import Pool as ThreadPool
import requests
import re
import time

def spider(url):
    print(url)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
    html = requests.get(url, headers=headers) #伪装成浏览器
    selector = etree.HTML(html.text) #将网页html变成树结构，用于xpath
    content = selector.xpath('//figure[@class="post-image "]') #提取figure标签
    for each in content:
        tmp = each.xpath('a/img/@src')#把img标签的src属性提取出来
        pic = requests.get(tmp[0])#访问图片
        print('downloading: ' + tmp[0])
        string = re.search('\d+/\d+/(.*?)\\.jpg', str(tmp[0])).group(1) #正则表达式匹配图片名字
        fp=open('pic2\\'+string+'.jpg','wb')#放到pic2文件夹内，要自己创建
        fp.write(pic.content)
        fp.close()
if __name__ == '__main__':
    pool = ThreadPool(2) #双核电脑
    tot_page = []
    for i in range(1,11): #提取1到10页的内容
        link = 'http://hotpics.cc/page/' + str(i)
        tot_page.append(link)
    pool.map(spider, tot_page)#多线程工作
    pool.close()
    pool.join()
