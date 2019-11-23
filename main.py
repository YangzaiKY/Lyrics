import re
from urllib.parse import quote
from get_lyrics import GetLyrics

if __name__ == '__main__':
    # 歌曲名
    song_name = '感谢你曾来过'
    # 歌词网站链接
    encode_name = quote(song_name, encoding='utf-8')

    # 在百度百科中找歌词
    # website = 'https://baike.baidu.com/item/%s' % encode_name
    # 在魔镜歌词网找歌词
    website = 'http://mojim.com/%s.html?g3' % encode_name
    # 背景图片链接
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191113-1573600574832032886.jpg'
    # 蓝色泡泡背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574287876026077350.jpg'
    # 狗狗背景
    # background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574289857357041277.jpg'
    # 爱心背景
    background_image = 'https://image.ipaiban.com/upload-ueditor-image-20191121-1574293686970012420.jpg'
    
    GL = GetLyrics(song_name)
    GL.get_options_from_mojim(website)
    # GL.get_html(website)
    # GL.get_lyrics()
    # GL.add_style(background_image)
