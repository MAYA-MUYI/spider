import requests
import json
import time
import re
import os
import sys

def func(name,page):
    starturl="https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&searchid=55220274338984511&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&p=1&n=20&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0"
    starturl = re.sub(r"p=1", "p={0}", starturl)
    starturl = starturl.format(page)
    headers = {
    "cookie": 'RK=51FHFw4aE8; pgv_pvi=8430643200; ptcz=83cfc479ce75c5a1416df7d87136166109888f38587d9944738abca7ab77d17c; tvfe_boss_uuid=e4ba183f02ae980f; pgv_pvid=3169027098; pgv_pvid_new=2426636288_14882e87533; mobileUV=1_15f666e2b04_e8a50; pac_uid=1_1278077260; eas_sid=l1C5q306s9W2d845F9u7f1K1U6; ptui_loginuin=40370953; o_cookie=1278077260; luin=o1278077260; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221669eddcdc5156-0905303c6ff588-7d113749-1049088-1669eddcdc83f8%22%2C%22%24device_id%22%3A%221669eddcdc5156-0905303c6ff588-7d113749-1049088-1669eddcdc83f8%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lskey=00010000a5727043706a88a2aebf6044daf687035fcc0804760fd13cac0729275356f7aa88d5157b46210ea6; LW_sid=y1s5J425D4j7u9N1Q8Q0j2k383; LW_uid=p1q5u4d584A7f971l820z2k3M9; ts_uid=4705118039; yq_index=0; uin=o1278077260; skey=@mXN9mj3as; p_uin=o1278077260; pt4_token=cVwioR9KifEllUyD2CPEXz692iNhDH8JE-YwH*5TlRY_; p_skey=BE7HSxnTeFIPwrO6sJ*YXyA1xKGxT072f5YAo919LSY_; yqq_stat=0; pgv_si=s3828307968; pgv_info=ssid=s3773836208; ts_last=y.qq.com/n/yqq/toplist/4.html; ts_refer=link.zhihu.com/%3Ftarget%3Dhttps%253A//y.qq.com/n/yqq/toplist/4.html%2523stat%253Dy_new.toplist.menu.4',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3493.3 Safari/537.36'
    }
    params = {
        "w": name
    }
    res = requests.get(url=starturl, params=params, headers=headers)
    res = res.text
    res = json.loads(res)
    songname=[]
    songmid=[]
    for i in res["data"]["song"]["list"]:
        songmid.append(i["file"]["media_mid"])
        songname.append(i["name"])
    mid_name= dict(zip(songmid, songname))
    if mid_name == {}:
        sys.exit("爬取结束")
    for j in mid_name:
        vkey_url ="https://u.y.qq.com/cgi-bin/musicu.fcg?-=getplaysongvkey05137740976859173&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq.json&needNewCode=0&data=%7B%22req%22%3A%7B%22module%22%3A%22CDN.SrfCdnDispatchServer%22%2C%22method%22%3A%22GetCdnDispatch%22%2C%22param%22%3A%7B%22guid%22%3A%22953482270%22%2C%22calltype%22%3A0%2C%22userip%22%3A%22%22%7D%7D%2C%22req_0%22%3A%7B%22module%22%3A%22vkey.GetVkeyServer%22%2C%22method%22%3A%22CgiGetVkey%22%2C%22param%22%3A%7B%22guid%22%3A%22953482270%22%2C%22songmid%22%3A%5B%22{0}%22%5D%2C%22songtype%22%3A%5B0%5D%2C%22uin%22%3A%220%22%2C%22loginflag%22%3A1%2C%22platform%22%3A%2220%22%7D%7D%2C%22comm%22%3A%7B%22uin%22%3A0%2C%22format%22%3A%22json%22%2C%22ct%22%3A24%2C%22cv%22%3A0%7D%7D".format(j)
        res02 = requests.get(url=vkey_url,headers=headers)
        time.sleep(0.3)
        res02 = res02.text
        res02 = json.loads(res02)
        try:
            vkey = res02["req_0"]["data"]["midurlinfo"][0]["purl"]
        except:
            continue
        url = "http://dl.stream.qqmusic.qq.com/"+vkey
        songer = name
        path = "music/"+songer
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        try:
            filename = "music/" + songer+"/"+ mid_name[j] + ".m4a"
            res03=requests.get(url=url, headers=headers)
            with open(filename, "wb") as f:
                f.write(res03.content)
                print("-----------"+mid_name[j]+"--------ok")
        except:
            continue

name=input("歌手(name)")


while True:
    for page in range(1, 100):
        func(name=name, page=page)
        print("第%d页下载完成" % page)























