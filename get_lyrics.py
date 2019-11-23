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

        self.contents = []
        self.lyrics_websites = []

    def set_song_name(self, song_name):
        if song_name:
            self.song_name = song_name
                
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
                
        html = urllib.request.urlopen(html_request)
        data = html.read().decode(charset, errors='ignore')
        return data

    def get_data_from_baidu(self, url):
        data = self.get_html(url)

        with open('search_result_baidu.txt', 'w') as f:
            # if self.current_website and self.current_website == self.websites[3]:
            #     new_data = re.sub('>', '>\n', data)
            #     f.write(new_data)
            f.write(data)
        self.get_lyrics()

    def get_options_from_mojim(self, url):
        data = self.get_html(url)

        with open('search_result_mojim.txt', 'w') as f:
            f.write(data)

        with open('search_result_mojim.txt', 'r') as f:
            temp_content = ''
            # is_content = False
            is_result = False
            for line in f:
                if '</dd>' in line:
                    # is_content = False
                    is_result = False
                if '<dd class="mxsh_dd' in line:
                    temp = re.search(r'(?<=<dd class="mxsh_dd).+?(?=")', line)
                    # if temp and temp.group() == '0':
                    #     menu = []
                    #     is_content = True
                    if temp and temp.group() != '0':
                        if temp_content:
                            self.contents.append(temp_content.strip('--'))
                        temp_content = ''
                        is_result = True
                # if is_content and '<span class="mxsh_ss' in line and '<span class="mxsh_ss1">' not in line:
                #     temp = re.search(r'(?<=>)[^>]+?(?=<)', line)
                #     if temp:
                #         menu.append(temp.group().strip())
                if is_result and '<span class="mxsh_ss' in line and '<span class="mxsh_ss1">' not in line:
                    temp = re.search(r'(?<=<span class="mxsh_ss).+?(?=")', line)
                    if '<span class="mxsh_ss4">' in line:
                        temp_ = re.search(r'(?<=>)[^>.]+?(?=<)', line)
                        temp_href = re.search(r'(?<=href=").+?(?=")', line)
                        if temp_href:
                            self.lyrics_websites.append('http://mojim.com'+temp_href.group())
                    else:
                        temp_ = re.search(r'(?<=>)[^>]+?(?=<)', line)
                    if temp and temp_:
                        temp_content += temp_.group().strip() + '--'
            if temp_content:
                self.contents.append(temp_content.strip('__'))

    def get_options_from_d777(self, url):
        data = self.get_html(url)

        with open('search_result_d777.txt', 'w') as f:
            f.write(data)

        with open('search_result_d777.txt', 'r') as f:
            for line in f:
                if '<div class="neirong">' in line and '</div>' in line:
                    temp = re.findall(r'(?<=<li>).+?(?=>)', line)
                    for i in temp:
                        self.contents.append(re.sub('歌词', ' ', re.search(r'(?<=title=").+?(?=")', i).group()))
                        self.lyrics_websites.append('http://geci.d777.com'+re.search(r'(?<=href=").+?(?=")', i).group())

    def get_option_from_user(self, option):
        if self.contents:
            url = self.lyrics_websites[option]
            data = self.get_html(url)
            with open('chosen_result.txt', 'w') as w:
                w.write(data)
            self.get_lyrics()
            return True
        else:
            return False

    @staticmethod
    def get_lyrics_from_baidu():
        with open('search_result_baidu.txt', 'r') as f:
            with open('lyrics.txt', 'w', encoding='utf-8') as w:
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
                            w.write(temp.group() + '<br/>')
                if not lyrics_found:
                    lyrics = False
                    for line in temp_file:
                        if '<dl' in line or '<dt' in line or '<dd' in line or '<ul' in line:
                            lyrics = False
                        if '<div class="para" label-module="para">' in line and '歌曲歌词' in line:
                            lyrics = True
                        if lyrics and '<div class="para" label-module="para">' in line and '歌曲歌词' not in line:
                            w.write(re.search(r'(?<=<div class="para" label-module="para">).+?(?=<)', line).group() + '<br/>')

    @staticmethod
    def get_lyrics_from_mojim():
        with open('lyrics.txt', 'w') as w:
            with open('chosen_result.txt', 'r') as f:
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

    @staticmethod
    def get_lyrics_from_d777():
        with open('lyrics.txt', 'w') as w:
            with open('chosen_result.txt', 'r') as f:
                lyrics = False
                for line in f:
                    if lyrics:
                        temp = re.sub('<br>', '<br/>', line)
                        if temp:
                            w.write(temp)
                            lyrics = False
                    if '<div class="neirong">' in line:
                        lyrics = True

    def get_lyrics(self):
        if self.current_website and self.current_website == self.websites[0]:
            self.get_lyrics_from_baidu()

        elif self.current_website and self.current_website == self.websites[1]:
            self.get_lyrics_from_mojim()

        # elif self.current_website and self.current_website == self.websites[2]:
        #     lyrics = False
        #     for line in f:
        #         if '</div>' in line:
        #             lyrics = False
        #         if '<div class="txtgc" id="txtgc">' in line:
        #             lyrics = True
        #         if lyrics:
        #             if '<div class="txtgc" id="txtgc">' in line:
        #                 w.write(re.search(r'(?<=">).+?(?=<)', line).group() + '<br/>')
        #                 continue
        #             w.write(re.search(r'.+?(?=<)', line).group() + '<br/>')

        # elif self.current_website and self.current_website == self.websites[3]:
        #     lyrics = False
        #     for line in f:
        #         if '</div>' == line:
        #             lyrics = False
        #         if '<div class="css-8qbqv4">' in line:
        #             lyrics = True
        #         if lyrics:
        #             temp = re.search(r'.+(?=</div>)', line)
        #             if temp:
        #                 w.write(temp.group() + '<br/>')

        elif self.current_website and self.current_website == self.websites[4]:
            self.get_lyrics_from_d777()

        # elif self.current_website and self.current_website == self.websites[5]:
        #     lyrics = False
        #     for line in f:
        #         if '</div>' in line:
        #             lyrics = False
        #         if '<div class="lrc_main">' in line:
        #             lyrics = True
        #             continue
        #         if lyrics:
        #             w.write(re.sub('<br />', '<br/>', line).strip())

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
