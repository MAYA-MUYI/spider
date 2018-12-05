# -*- coding:utf-8 -*-
import urllib
import urllib.request
import time

def validateIp(ip, port):
    user_agent = " Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36"
    headers = {'User-Agent': user_agent}
    proxy = {'http':'http://%s:%s' %(ip, port)}

    #代理设置
    proxy_handler = urllib.request.ProxyHandler(proxy)
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)

    #请求网址
    validateUrl = 'https://www.baidu.com'
    req = urllib.request.Request(url=validateUrl, headers=headers)
    #延时，等待反馈结果
    time.sleep(4)

    #判断结果
    try:
        res = urllib.request.urlopen(req)
        # 延时，等待反馈结果
        time.sleep(2)
        content = res.read()
        #写入文件
        if content:
            print("is ok")
            with open('data2.txt','a') as wd:
                wd.write(ip+':'+port+'\n')
        else:
            print('未通过')
    except urllib.request.URLError as e:
        print(e.reason)

if __name__ == '__main__':
    with open('proxy_data2.txt', 'r') as rd:
        iplist = rd.readlines()
        for ip in iplist:
            validateIp(ip.split(':')[0],ip.split(':')[1])
