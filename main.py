import re
from get_lyrics import GetLyrics

if __name__ == '__main__':
    # 歌曲名
    song_name = '校花隔壁的流川枫'
    # 歌词网站链接
    a = '天亮了'.encode(encoding='gb2312')
    print(a)
    website = 'https://baike.baidu.com/item/%E5%A4%A9%E4%BA%AE%E4%BA%86/3158366'
    # 背景图片链接
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191113-1573600574832032886.jpg'
    # 蓝色泡泡背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574287876026077350.jpg'
    # 狗狗背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574289857357041277.jpg'
    # 爱心背景
    background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574293686970012420.jpg'
    
    GL = GetLyrics(song_name)
    GL.get_html(website)
    GL.get_lyrics()
    GL.add_style(background_image)
