import urllib.request

def main():
    print ("downloading with urllib")
    # url = 'http://www.wzsky.net/img2013/uploadimg/20130906/1216294.jpg'
    # url = 'http://music.163.com/song/media/outer/url?id=436514312.mp3'
    url = "http://dl.stream.qqmusic.qq.com/M5000033P66R0qEtlT.mp3?vkey=8B72FD21C0AE21B277F73750DA12D8B6D8D0A39FD691B41CC8D9948D7DC0FD9303558F150D792D2AD37EEFD8E8016D3DC4DF1BCD238034D7&guid=4831899136&fromtag=64"
    f = urllib.request.urlopen(url)
    data = f.read()
    # with open("d:/color/1216294.mp3", "wb") as code:
    with open("C:/Users/asus/Desktop/tes.mp3", 'wb') as code:
        code.write(data)

if __name__ == '__main__':
    main()