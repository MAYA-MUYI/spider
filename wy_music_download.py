import requests, os, time, sys, re
import urllib
from scrapy.selector import Selector

#根据专辑
class wangyiyun():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Referer': 'http://music.163.com/'}
        self.main_url='http://music.163.com/'
        self.session = requests.Session()
        self.session.headers=self.headers

    def get_songurls(self,playlist):
        '''获取歌单链接"'''
        url=self.main_url+'playlist?id=%d'% playlist
        re= self.session.get(url)
        sel=Selector(text=re.text)
        songurls=sel.xpath('//ul[@class="f-hide"]/li/a/@href').extract()
        return songurls

    def get_songinfo(self,songurl):
        url=self.main_url+songurl
        re=self.session.get(url)
        sel=Selector(text=re.text)
        song_id = url.split('=')[1]
        song_name = sel.xpath("//em[@class='f-ff2']/text()").extract_first()
        singer= '&'.join(sel.xpath("//p[@class='des s-fc4']/span/a/text()").extract())
        songname=singer+'-'+song_name
        return str(song_id), songname

    def download_song(self, songurl, dir_path):
        '''根据歌曲url，下载mp3文件'''
        song_id, songname = self.get_songinfo(songurl)  # 根据歌曲url得出ID、歌名
        song_url = 'http://music.163.com/song/media/outer/url?id=%s.mp3'%song_id
        path = dir_path + os.sep + songname + '.mp3'  # 文件路径
        urllib.request.urlretrieve(song_url, path)
        # requests.urlretrieve(song_url, path)  # 下载文件

    def work(self, playlist):
        songurls = self.get_songurls(playlist)  # 输入歌单编号，得到歌单所有歌曲的url
        dir_path = r'C:\\Users\\asus\\Desktop'
        for songurl in songurls:
            self.download_song(songurl, dir_path)  # 下载歌曲

if __name__ == '__main__':
    songs_id = int(input("请输入歌单ID："))
    d = wangyiyun()
    # d.work(2480922572)
    d.work(songs_id)