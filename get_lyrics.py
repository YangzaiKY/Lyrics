import re
import ssl
import urllib.request

class GetLyrics:
    def __init__(self, song_name=None):
        self.websites = ['baike.baidu.com',
                         'mojim.com',
                         'www.yue365.com',
                         'www.rapzh.com',
                         'geci.d777.com',
                         'emumo.xiami.com'
                         ]
        self.current_website = None
        self.song_name = song_name

        ssl._create_default_https_context = ssl._create_unverified_context
        self.headers = {
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
                        }
                
    def get_html(self, url):
        for i in range(len(self.websites)):
            if self.websites[i] in url:
                 self.current_website = self.websites[i]

        html_request = urllib.request.Request(url, headers=self.headers)
        html = urllib.request.urlopen(html_request)
        charset = 'utf-8'
        charset_test = html.read(2000).decode(charset, errors='ignore')
        if 'charset' in charset_test.lower():
            temp = re.search(r'(?<=charset=).+?(?=")', charset_test, re.I)
            if temp:
                charset = temp.group().strip('"')
                print('数据集：', charset)
                
        html = urllib.request.urlopen(html_request)
        data = html.read().decode(charset, errors='ignore')

        with open('data.txt', 'w') as f:
            if self.current_website and self.current_website == self.websites[3]:
                new_data = re.sub('>', '>\n', data)
                f.write(new_data)
            else:
                f.write(data)

    def get_options_from_mojim(self, url):
        html_request = urllib.request.Request(url, headers=self.headers)
        html = urllib.request.urlopen(html_request)

        charset = 'utf-8'
        get_charset = html.read(2000).decode(charset, errors='ignore')
        if 'charset' in get_charset.lower():
            temp = re.search(r'(?<=charset=).+?(?=")', get_charset, re.I)
            if temp:
                charset = temp.group().strip('"')
                print('网站所用数据集：', charset)

        html = urllib.request.urlopen(html_request)
        data = html.read().decode(charset, errors='ignore')

        with open('search_result.txt', 'w') as f:
            f.write(data)

        contents = []
        lyrics_websites = []
        with open('search_result.txt', 'r') as f:
            temp_content = None
            is_content = False
            is_result = False
            for line in f:
                if '</dd>' in line:
                    is_content = False
                    is_result = False
                if '<dd class="mxsh_dd' in line:
                    temp = re.search(r'(?<=<dd class="mxsh_dd).+?(?=")', line)
                    if temp and temp.group() == '0':
                        menu = []
                        is_content = True
                    if temp and temp.group() != '0':
                        if temp_content:
                            contents.append(temp_content)
                        temp_content = {}
                        is_result = True
                if is_content and '<span class="mxsh_ss' in line and '<span class="mxsh_ss1">' not in line:
                    temp = re.search(r'(?<=>)[^>]+?(?=<)', line)
                    if temp:
                        menu.append(temp.group().strip())
                if is_result and '<span class="mxsh_ss' in line and '<span class="mxsh_ss1">' not in line:
                    temp = re.search(r'(?<=<span class="mxsh_ss).+?(?=")', line)
                    if '<span class="mxsh_ss4">' in line:
                        temp_ = re.search(r'(?<=>)[^>.]+?(?=<)', line)
                        temp_href = re.search(r'(?<=href=").+?(?=")', line)
                        if temp_href:
                            lyrics_websites.append('http://mojim.com'+temp_href.group())
                    else:
                        temp_ = re.search(r'(?<=>)[^>]+?(?=<)', line)
                    if temp and temp_:
                        temp_content[menu[int(temp.group().strip())-2]] = temp_.group().strip()
            contents.append(temp_content)
        for i, j in zip(contents, lyrics_websites):
            print(i)
            print(j)

    def get_lyrics(self):
        lyrics = False
        with open('data.txt', 'r', encoding='utf-8') as f:
            with open('lyrics.txt',  'w', encoding='utf-8') as w:
                if self.current_website and self.current_website == self.websites[0]:
                    lyrics = False
                    lyrics_found = False
                    temp_file = []
                    for line in f:
                        temp_file.append(line)
                        if '<h2 class="title-text"><span class="title-prefix">' in line:
                            lyrics = False
                        find_lyrics = re.search(r'(?<=<h2 class="title-text"><span class="title-prefix">).+?(?=歌曲歌词)', line)
                        if find_lyrics:
                            lyrics = True
                            lyrics_found = True
                        if lyrics:
                            temp = re.search(r'(?<=<div class="para" label-module="para">).+?(?=<)', line)
                            if temp:
                                w.write(temp.group()+'<br/>')
                    if not lyrics_found:
                        lyrics = False
                        for line in temp_file:
                            if '<dl' in line or '<dt' in line or '<dd' in line or '<ul' in line:
                                lyrics = False
                            if '<div class="para" label-module="para">' in line and '歌曲歌词' in line:
                                lyrics = True
                            if lyrics and '<div class="para" label-module="para">' in line and '歌曲歌词' not in line:
                                w.write(re.search(r'(?<=<div class="para" label-module="para">).+?(?=<)', line).group() + '<br/>')

                elif self.current_website and self.current_website == self.websites[1]:
                    for line in f:
                        if "<dd id='fsZx3' class='fsZx3'>" in line:
                            temp_lyrics = re.search(r"(?<=<dd id='fsZx3' class='fsZx3'>).+", line).group()
                            temp_lyrics = temp_lyrics.split('<br />')
                            lyrics = []
                            for item in temp_lyrics:
                                if item == '' or '[' in item or '<' in item or '更多更详尽歌词' in item:
                                    continue
                                lyrics.append(item)
                            lyrics = '<br/>'.join(lyrics)
                            w.write(lyrics)
                            
                elif self.current_website and self.current_website == self.websites[2]:
                    lyrics = False
                    for line in f:
                        if '</div>' in line:
                            lyrics = False
                        if '<div class="txtgc" id="txtgc">' in line:
                            lyrics = True
                        if lyrics:
                            if '<div class="txtgc" id="txtgc">' in line:
                                w.write(re.search(r'(?<=">).+?(?=<)', line).group() + '<br/>')
                                continue
                            w.write(re.search(r'.+?(?=<)', line).group() + '<br/>')

                elif self.current_website and self.current_website == self.websites[3]:
                    lyrics = False
                    for line in f:
                        if '</div>' == line:
                            lyrics = False
                        if '<div class="css-8qbqv4">' in line:
                            lyrics = True
                        if lyrics:
                            temp = re.search(r'.+(?=</div>)', line)
                            if temp:
                                w.write(temp.group() + '<br/>')

                elif self.current_website and self.current_website == self.websites[4]:
                    lyrics = False
                    for line in f:
                        if lyrics:
                            temp = re.sub('<br>', '<br/>', line)
                            if temp:
                                w.write(temp)
                                lyrics = False
                        if '<div class="neirong">' in line:
                            lyrics = True

                elif self.current_website and self.current_website == self.websites[5]:
                    lyrics = False
                    for line in f:
                        if '</div>' in line:
                            lyrics = False
                        if '<div class="lrc_main">' in line:
                            lyrics = True
                            continue
                        if lyrics:
                            w.write(re.sub('<br />', '<br/>', line).strip())

    def add_style(self, background_url):
        with open('lyrics.txt', 'r', encoding='utf-8') as f:
            with open('lyrics_with_style.txt', 'w', encoding='utf-8') as w:
                w.write('<section style="background-image:url(' + background_url +
                        ');background-position:center;background-size:100%;background-repeat:repeat-y;">\n')
                w.write('<p style="text-align:center">\n')
                w.write('<strong><span style="font-size: 24px;">%s</span></strong><br/>' % self.song_name)
                w.write('<strong><span style="font-size: 20px;">苏二喜</span></strong><br/><br/>')

                for line in f:
                    w.write(line)
                w.write('<br/><em style="font-size: 14px; color: rgb(255, 41, 65);"><strong>*&nbsp;'
                        '进入公众号首页点击歌单，收听更多好听走心的歌</strong></em>')
                w.write('</p>\n')
                w.write('</section>\n')
