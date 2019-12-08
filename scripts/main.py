from tkinter import *

from GUI import LyricsGUI

if __name__ == '__main__':
    root = Tk()
    root.geometry('800x600')

    App = LyricsGUI(root)

    root.mainloop()

    # 背景图片链接
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191113-1573600574832032886.jpg'
    # 蓝色泡泡背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574287876026077350.jpg'
    # 狗狗背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574289857357041277.jpg'
    # 爱心背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574293686970012420.jpg'
    # 花背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191205-1575543817403027944.jpeg'
    # 粉红背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191205-1575544598065068405.jpg'

    # GL.get_html(website)
    # GL.get_lyrics()
    # GL.add_style(background_image)
