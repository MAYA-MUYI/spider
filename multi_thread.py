import requests
import threading
from lxml import etree
import urllib.request
import os


URL_LIST = []
PIC_LIST = []
gLock = threading.Lock()

for i in range(10):
    url = "https://www.doutula.com/photo/list/?page={}".format(i)
    URL_LIST.append(url)
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36"
}

def get_Url():
    while True:
        gLock.acquire()
        if len(URL_LIST) == 0:
            gLock.release()
            break
        else:
            pic_url = URL_LIST.pop()
            gLock.release()
            html = requests.get(pic_url, headers).text
            etr = etree.HTML(html)
            imgs = etr.xpath('//a[@class="col-xs-6 col-sm-3"]/img/@data-original')
            gLock.acquire()
            for img in imgs:
                PIC_LIST.append(img)
            gLock.release()

    return PIC_LIST
def download():
    PIC_LIST = get_Url()
    while True:
        gLock.acquire()
        if len(PIC_LIST) == 0:
            gLock.release()
            break
        else:
            pic_url = PIC_LIST.pop()
            gLock.release()
            f = urllib.request.urlopen(pic_url)
            data = f.read()
            pic_name = pic_url.split('/')[-1]
            path = os.path.join('images', pic_name)
            filename = os.getcwd() + '\\' + path
            print("pic_name:", filename)
            with open(filename.replace('\\', '/'), 'wb') as code:
                code.write(data)

if __name__ == '__main__':
    for x in range(2):
        th = threading.Thread(target=get_Url)
        th.start()
    for y in range(2):
        th = threading.Thread(target=download)
        th.start()
