from wand.image import Image as wandImage	# pdf –> jpeg
from PIL import Image as pillowIMage	# PyOCR需要
import pyocr.builders		# OCR识别
import io				# 将Wand处理结果传给给Pillow
import pprint			# 美美的打印出来
import os
import re
import random
from threading import Thread
from multiprocessing import Process

#读取文件名
def eachFile(filepath):
    file_pash_list = []
    pathDir = os.listdir(filepath)
    for allDir in pathDir:
        child = os.path.join('%s\%s'%(filepath,allDir))
        file_pash_list.append(child)
    return file_pash_list

def ocr(path):
    # PyOCR初始化
    tool = pyocr.get_available_tools()[0]
    # 获得OCR内核工具，这里用的是Tesseract
    lang = tool.get_available_languages()[0]
    # 获得识别用语言，这里用的是简体中文，参见20.2 PyOCR的初始化程序

    req_image = []	# 存放pdf转换过来的图片二进制数据流
    final_text = []	# 存放识别结果，每个元素是每一页识别出来的文字

    ima_pdf = wandImage(filename='{}'.format(path), resolution=200)
    # 打开pdf文件，生成wand图片对象。分辨率设为300，设高分辨率有助于提高识别率
    image_jpeg = ima_pdf.convert('jpeg')
    # pdf文件转成图片，实际上是个图片序列，序列的长度与pdf的页数相同

    for img in image_jpeg.sequence:	# 遍历图片序列的每页图片
        img_page = wandImage(image=img)	# 生成为wand图片对象
        img_page.type = 'grayscale'		# 转成灰度模式有助于OCR识别文字
        req_image.append(img_page.make_blob('jpeg'))
    # 转成二进制数据流放进列表

    for img in req_image:		# 一页一页OCR识别文字
        # print(img)
        text = tool.image_to_string(
            pillowIMage.open(io.BytesIO(img)),
        # io.BytesIO()从内存中读入二进制数据流
            lang=lang,	# 识别语言
            builder=pyocr.builders.TextBuilder()	# 识别器
        )
        final_text.append(text)		# 识别出来的结果添进列表

    # final_str = re.sub('微信.*/d+','66666666',final_text)
    final_str = "".join(final_text)

    return re.sub("微信([a-z]+\d+|\d+)|微售\s* \d+","",final_str)
    # print(final_str)




def save(content,file_name):
    r = open(r"C:\Users\Administrator\Desktop\关键词库\电子书长尾词.txt", "r", encoding='utf-8')
    lines = r.readlines()  # 读取全部内容
    r.close()
    lines_ran = [x.strip() for x in random.sample(lines, 3)]

    with open(r'C:\Users\Administrator\Desktop\输出\{}(简介_书评_在线阅读 pdf mobi epub).txt'.format(file_name),'w',encoding='utf-8') as f:
        contents = "<h2>{}</h2>".format(file_name)+content.strip()+"<p>电子书阅读相关:" + ','.join(lines_ran) + "</p>"
        f.write(contents)
        f.close()


def run():
    paths = eachFile(r'C:\Users\Administrator\Desktop\输入pdf')

    for inx,path in enumerate(paths):

        file_name = path.split("\\")[-1].split(".")[-2]
        content = ocr(path)
        save(content,file_name)
        print('第{}个文件,处理完成....'.format(inx+1))
        # print(file_name)





if __name__ == '__main__':
    run()

