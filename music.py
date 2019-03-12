#!/usr/bin/env python
# -*- coding：utf-8 -*-
'''
@author: maya
@contact: 1278077260@qq.com
@software: Pycharm
@file: music.py
@time: 2019/1/8 12:48
@desc:
'''
import json
import requests
import time
import os
import urllib

headers = {
        "cookie": 'RK=51FHFw4aE8; pgv_pvi=8430643200; ptcz=83cfc479ce75c5a1416df7d87136166109888f38587d9944738abca7ab77d17c; tvfe_boss_uuid=e4ba183f02ae980f; pgv_pvid=3169027098; pgv_pvid_new=2426636288_14882e87533; mobileUV=1_15f666e2b04_e8a50; pac_uid=1_1278077260; eas_sid=l1C5q306s9W2d845F9u7f1K1U6; ptui_loginuin=40370953; o_cookie=1278077260; luin=o1278077260; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221669eddcdc5156-0905303c6ff588-7d113749-1049088-1669eddcdc83f8%22%2C%22%24device_id%22%3A%221669eddcdc5156-0905303c6ff588-7d113749-1049088-1669eddcdc83f8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lskey=00010000a5727043706a88a2aebf6044daf687035fcc0804760fd13cac0729275356f7aa88d5157b46210ea6; LW_sid=y1s5J425D4j7u9N1Q8Q0j2k383; LW_uid=p1q5u4d584A7f971l820z2k3M9; ts_uid=4705118039; yq_index=0; uin=o1278077260; skey=@mXN9mj3as; p_uin=o1278077260; pt4_token=cVwioR9KifEllUyD2CPEXz692iNhDH8JE-YwH*5TlRY_; p_skey=BE7HSxnTeFIPwrO6sJ*YXyA1xKGxT072f5YAo919LSY_; yqq_stat=0; pgv_si=s3828307968; pgv_info=ssid=s3773836208; ts_last=y.qq.com/n/yqq/toplist/4.html; ts_refer=link.zhihu.com/%3Ftarget%3Dhttps%253A//y.qq.com/n/yqq/toplist/4.html%2523stat%253Dy_new.toplist.menu.4',
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'

    }

def getHtml(start_url):

    try:
        r = requests.get(start_url, headers=headers)
        r.encoding = r.apparent_encoding


        text = json.loads(r.text)
        return text
    except:
        return ""

def getSongMid(html):

    songmid = []
    for tid in html['songlist']:
        songmid.append([tid['data']['songmid'], tid['data']['songname']])
    return songmid

def getSong(html):
    start_index = 0
    while (True):
        start_num = start_index * 30
        num = 30
        start_index += 1
        update_key = html['update_time']  # 有些update_key为2018-5，而实际请求需要传递2018-05，因此需要转换下
        temp_key = update_key.split("_")
        if (len(temp_key) == 3):
            if len(temp_key[1]) == 1:
                update_key = temp_key[0] + '_0' + temp_key[1] + temp_key[2]
            elif len(temp_key[2]) == 1:
                update_key = temp_key[0] + temp_key[1] + '_0' + temp_key[2]
        page_url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date={0}&topid=4&type=top&song_begin={1}&song_num=30&g_tk=1154346586&loginUin=1278077260&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0".format(
            update_key, start_num)
        json_text = getHtml(page_url)
        songinfo = getSongMid(json_text)
        if len(songinfo) == 0:
            break
        for sid in songinfo:
            vkey = getVkey(sid[0])#获取每首音乐的vkey
            saveMusic(sid[0],vkey,sid[1])#保存此音乐
            time.sleep(1)#休眠1秒，防止被服务器过滤掉

def getVkey(songmid):
    vkey_url = "https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey05137740976859173&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%22953482270%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22953482270%22%2C%22songmid%22%3A%5B%22{0}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D".format(songmid)
    res = requests.get(url=vkey_url)
    time.sleep(0.5)
    res02 = json.loads(res.text)
    vkey = res02["req_0"]["data"]["midurlinfo"][0]["purl"]
    return vkey



def saveMusic(songmid, vkey, name):

    headers['Host'] = 'dl.stream.qqmusic.qq.com'
    url = "http://dl.stream.qqmusic.qq.com/" + vkey
    res = requests.get(url, headers=headers, stream=True)
    filename = 'song/{0}.m4a'.format(name.replace("?", "").replace("/", "_").replace("\\", "_").replace("\"", ""))

    print("*****    正在下载    *****")
    print(url)
    print("*****歌曲：{}".format(name.replace("?", "").replace("/", "_").replace("\\", "_").replace("\"", "")))

    with open(filename, 'wb') as f:
        f.write(res.raw.read())
    if(urllib.request.urlopen(url).getheader('Content-Length') > 0):
        print("成功下载歌曲：{}".format(name.replace("?", "").replace("/", "_").replace("\\", "_").replace("\"", "")))
        # size = urllib.request.urlopen(url).getheader('Content-Length')
        # print(size)
    else:
        print("下载失败")
        os.remove(filename)

if __name__ == '__main__':
    start_url = "https://c.y.qq.com/v8/fcg-bin/fcg_v8_toplist_cp.fcg?tpl=3&page=detail&date=2019-01-08&topid=4&type=top&song_begin=0&song_num=30&g_tk=1154346586&loginUin=1278077260&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
    text = getHtml(start_url)
    getSong(text)

