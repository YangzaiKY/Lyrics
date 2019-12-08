import os
import re
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from urllib.parse import quote

import requests

from get_lyrics import GetLyrics


class LyricsGUI:
    def __init__(self, master):
        self.master = master
        self.GL = GetLyrics()
        self.source = ['百度百科', '魔镜网', '365音乐网', '第七空间']

        self.frame = Frame(self.master)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.init_widgets()

        self.background_image_url = None

    def init_widgets(self):
        ttk.Label(self.frame, text='歌名：', font=(None, 12)).place(relx=0.02, rely=0.01, relwidth=0.06, relheight=0.05)
        self.song_name_entry = ttk.Entry(self.frame,
                                         font=(None, 12))
        self.song_name_entry.place(relx=0.12, rely=0.009, relwidth=0.3, relheight=0.06)

        ttk.Label(self.frame, text='搜索源：', font=(None, 12)).place(relx=0.02, rely=0.08, relwidth=0.1, relheight=0.05)
        self.source_var = StringVar()
        self.source_cb = ttk.Combobox(self.frame,
                                      textvariable=self.source_var,
                                      font=(None, 12),
                                      state='readonly')
        self.source_cb.place(relx=0.12, rely=0.08, relwidth=0.3, relheight=0.06)
        self.source_cb['values'] = self.source
        self.source_var.set('百度百科')

        ttk.Button(self.frame,
                   text='搜索',
                   command=self.start_search).place(relx=0.45, rely=0.01, relwidth=0.1, relheight=0.12)

        ttk.Label(self.frame,
                  text='背景图片: ',
                  font=(None, 12)).place(relx=0.02, rely=0.15, relwidth=0.1, relheight=0.05)

        self.background_image_entry =  ttk.Entry(self.frame,
                                                 font=(None, 12))
        self.background_image_entry.place(relx=0.12, rely=0.15, relwidth=0.25, relheight=0.05)

        ttk.Button(self.frame,
                   text='导入本地背景图片',
                   command=self.choose_bg_image).place(relx=0.37, rely=0.15, relwidth=0.18, relheight=0.05)

        self.song_list_var = StringVar()
        self.song_list = Listbox(self.frame,
                                 listvariable=self.song_list_var,
                                 selectmode='single')
        self.song_list.place(relx=0.02, rely=0.2, relwidth=0.53, relheight=0.78)
        self.song_list_scrollbar = ttk.Scrollbar(self.frame, command=self.song_list.yview)
        self.song_list_scrollbar.place(relx=0.55, rely=0.2, relwidth=0.02, relheight=0.78)
        self.song_list.configure(yscrollcommand=self.song_list_scrollbar.set)
        self.song_list.bind('<Double-1>', self.open_lyrics)

        ttk.Label(self.frame,
                  text='歌词',
                  font=(None, 20),
                  anchor=CENTER,
                  justify=CENTER).place(relx=0.65, rely=0.02, relwidth=0.25, relheight=0.1)

        self.lyrics_text = Text(self.frame,
                                font=(None, 12),
                                borderwidth=2)
        self.lyrics_text.place(relx=0.6, rely=0.15, relwidth=0.38, relheight=0.8)
        self.lyrics_text_scrollbar = ttk.Scrollbar(self.frame, command=self.lyrics_text.yview)
        self.lyrics_text_scrollbar.place(relx=0.98, rely=0.15, relwidth=0.02, relheight=0.8)
        self.lyrics_text.configure(yscrollcommand=self.lyrics_text_scrollbar.set)
        self.lyrics_text.insert(END, '欢迎使用本软件～')

    def start_search(self):
        self.song_list_var.set('')
        song_name = self.song_name_entry.get()
        self.GL.set_song_name(song_name)
        encode_name = quote(song_name, encoding='utf-8')

        source = self.source.index(self.source_var.get())
        if source == 0:
            # 在百度百科中找歌词
            website = 'https://baike.baidu.com/item/{}'.format(encode_name)
            self.GL.get_data_from_baidu(website)
            self.lyrics_text.delete('1.0', END)
            self.lyrics_text.insert(END, self.song_name_entry.get()+'\n\n')
            with open('../data/lyrics.txt', 'r') as f:
                for line in f:
                    self.lyrics_text.insert(END, re.sub('<br/>', '\n', line))
        elif source == 1:
            # 在魔镜歌词网找歌词
            website = 'http://mojim.com/{}.html?g3'.format(encode_name)
            self.GL.get_options_from_mojim(website)
            if not self.GL.contents:
                messagebox.showwarning(message='抱歉在此搜索源没有找到歌词，请尝试其它搜索源！')
            else:
                for item in self.GL.contents:
                    self.song_list.insert(END, item)
        elif source == 2:
            # 在365音乐网找歌词
            encode_name = quote(song_name, encoding='gb2312')
            website = 'http://my.yue365.com/ajax/Search.ashx?keyword={}&Page=1&type=song&jsoncallback=jsonp1575585078427&_=1575585085886'.format(encode_name)
            self.GL.get_options_from_yue365(website)
            if not self.GL.contents:
                messagebox.showwarning(message='抱歉在此搜索源没有找到歌词，请尝试其它搜索源！')
            else:
                for item in self.GL.contents:
                    self.song_list.insert(END, item)

        elif source == 3:
            # 在第七空间找歌词
            website = 'http://geci.d777.com/{}_s.html'.format(encode_name)
            self.GL.get_options_from_d777(website)
            if not self.GL.contents:
                messagebox.showwarning(message='抱歉在此搜索源没有找到歌词，请尝试其它搜索源！')
            else:
                for item in self.GL.contents:
                    self.song_list.insert(END, item)

    def choose_bg_image(self):
        image_path = filedialog.askopenfilename(title='选择背景图片',
                                                filetypes=[('JPG文件', '*.jpg'),
                                                           ('JPEG文件', '*.jpeg'),
                                                           ('GIF文件', '*.gif'),
                                                           ('PNG文件', '*.png')],
                                                initialdir='/Users/kangyangwu/Desktop')
        if len(image_path) > 0:
            temp = re.search(r'(?<=/)[^/]+$', image_path)
            if temp:
                image_name = temp.group()
                self.background_image_entry.insert(END, image_name)
            website = 'http://ipaiban.com/js/ueditor_minimalist/jsp/controller.jsp?action=uploadimage&encode=utf-8'

            if os.path.exists(image_path):
                file = {'file': open(image_path, 'rb')}

                headers = {
                          'Connection': 'keep-alive',
                          'Content-Length': '45077',
                          'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
                          }

                r = requests.post(website, headers=headers, files=file)

                with open('../data/image_url.txt', 'w') as f:
                    f.write(r.text)

                with open('../data/image_url.txt', 'r') as f:
                    for line in f:
                        if 'title' in line:
                            temp = re.search(r'(?<="title": ").+?(?=")', line)
                            if temp:
                                self.background_image_url = temp.group()

    def open_lyrics(self, event):
        index = self.song_list.curselection()
        if self.GL.get_option_from_user(index[0]):
            self.lyrics_text.delete('1.0', END)
            self.lyrics_text.insert(END, self.song_name_entry.get()+'\n\n')
            with open('../data/lyrics.txt', 'r') as f:
                for line in f:
                    self.lyrics_text.insert(END, re.sub('<br/>', '\n', line))

            background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191205-1575544598065068405.jpg'
            self.GL.add_style(self.background_image_url if self.background_image_url is not None else background_image)

