from tkinter import *
from tkinter import ttk
from urllib.parse import quote

from get_lyrics import GetLyrics


class LyricsGUI:
    def __init__(self, master):
        self.master = master
        self.GL = GetLyrics()
        self.source = ['百度百科', '魔镜网', '第七空间']

        self.frame = Frame(self.master)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.init_widgets()

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

        self.song_list_var = StringVar()
        self.song_list = Listbox(self.frame,
                                 listvariable=self.song_list_var,
                                 selectmode='single')
        self.song_list.place(relx=0.02, rely=0.15, relwidth=0.53, relheight=0.8)
        self.song_list_scrollbar = ttk.Scrollbar(self.frame, command=self.song_list.yview)
        self.song_list_scrollbar.place(relx=0.55, rely=0.15, relwidth=0.02, relheight=0.8)
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
        song_name = self.song_name_entry.get()
        self.GL.set_song_name(song_name)
        encode_name = quote(song_name, encoding='utf-8')

        source = self.source.index(self.source_var.get())
        if source == 0:
            # 在百度百科中找歌词
            website = 'https://baike.baidu.com/item/%s' % encode_name
            self.GL.get_data_from_baidu(website)
            self.lyrics_text.delete('1.0', END)
            self.lyrics_text.insert(END, self.song_name_entry.get()+'\n\n')
            with open('lyrics.txt', 'r') as f:
                for line in f:
                    self.lyrics_text.insert(END, re.sub('<br/>', '\n', line))
        elif source == 1:
            # 在魔镜歌词网找歌词
            website = 'http://mojim.com/%s.html?g3' % encode_name
            self.GL.get_options_from_mojim(website)
        elif source == 2:
            # 在第七空间找歌词
            website = 'http://geci.d777.com/%s_s.html' % encode_name
            self.GL.get_options_from_d777(website)

        for item in self.GL.contents:
            self.song_list.insert(END, item)

    def open_lyrics(self, event):
        index = self.song_list.curselection()
        if self.GL.get_option_from_user(index[0]):
            self.lyrics_text.delete('1.0', END)
            self.lyrics_text.insert(END, self.song_name_entry.get()+'\n\n')
            with open('lyrics.txt', 'r') as f:
                for line in f:
                    self.lyrics_text.insert(END, re.sub('<br/>', '\n', line))

