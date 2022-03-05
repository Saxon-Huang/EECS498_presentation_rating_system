import requests
import os
import csv


def do_load_media(url, path, num, year):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        # 循环接收视频数据
        while True:
            # 若文件已经存在，则断点续传，设置接收来需接收数据的位置
            if not year:
                if os.path.exists(path):
                    headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
                res = requests.get(url, stream=True, headers=headers)

                content_length = int(res.headers['content-length'])
                # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
                if content_length < pre_content_length or (
                        os.path.exists(path) and os.path.getsize(path) == content_length):
                    break
                pre_content_length = content_length

                # 写入收到的视频数据
                with open(path, 'ab') as file:
                    file.write(res.content)
                    file.flush()
                    print('receive data，file size : %d  total size:%d' %
                          (os.path.getsize(path), content_length))
            else:
                for i in range(2000, 2018):
                    if os.path.exists(path):
                        headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
                    url = url[:-32] + str(i) + url[-28:]
                    res = requests.get(url, stream=True, headers=headers)

                    content_length = int(res.headers['content-length'])
                    # 若当前报文长度小于前次报文长度，或者已接收文件等于当前报文长度，则可以认为视频接收完成
                    pre_content_length = content_length

                    # 写入收到的视频数据
                    with open(path, 'ab') as file:
                        file.write(res.content)
                        file.flush()
                        print('receive data，file size : %d  total size:%d' %
                              (os.path.getsize(path), content_length))

                    if content_length > 100:
                        break          
                break              
    except Exception as e:
        print(e)


def load_media(url, num, year):
    path = r'./audio/' + str(num) + ".mp3"
    do_load_media(url, path, num, year)
    pass


def main():
    f = csv.reader(open('ted_main.csv', 'r'))
    num = 0
    for info in f:
        if num == 0:
            num += 1
            continue
        yearunknown = False
        # SirKenRobinson_2006.mp3?apikey=acme-roadrunner'
        url = 'https://download.ted.com/talks/'
        post = "?apikey=acme-roadrunner"
        # print(info[3][:4])
        if info[3][:4] == "TED2":     # TED
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + ".mp3"
        elif info[3][:4] == "TEDG":  # TEDGlobal
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "G.mp3"
        elif info[3][:4] == "TEDS":  # TEDSalon
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "S.mp3"
        elif info[3][:4] == "TEDW":  # TEDWoman
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "W.mp3"
        elif info[3][:4] == "TED@":  # TED@
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "S.mp3"
        elif info[3] == "TEDM":  # TEDMED
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "P.mp3"
            yearunknown = True
        elif info[3][:4] == "TEDx":  # TEDx
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "X.mp3"
            yearunknown = True
        elif info[3] == "Chautauqua Institution":
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "P.mp3"
            yearunknown = True
        else:
            filename = ''.join(info[6].split(' ')) + \
                "_" + str(info[3][-4:]) + "S.mp3"
            yearunknown = True

        url = url + filename + post
        print(url)
        load_media(url, num, yearunknown)
        num += 1
        print(num, " finished")


if __name__ == '__main__':
    main()
