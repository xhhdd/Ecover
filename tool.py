# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import time
from timeit import timeit
from PIL import Image,ImageDraw,ImageFont
from  multiprocessing import Process
import create_cover

from create_cover import adjust_font
def create():
    content="测试文字1"
    # 生成一个白色底板
    bg=Image.new("RGB",(3840,2160),(255,255,255)) 
    # 绘制圆角底色
    round_bg=ImageDraw.Draw(bg)
    round_bg.rounded_rectangle([(80,80), (3760, 2080)],radius=80,fill='#80ed99')
    # 左侧区域圆
    left_area=ImageDraw.Draw(bg)
    left_area.ellipse([(600,780), (1200, 1380)],fill=(255,255,255))
    # 右侧矩形
    right_area=ImageDraw.Draw(bg)
    left_area.rounded_rectangle([(1500,120), (3720, 1960)],radius=80,fill=(255,255,255))
    # 字体
    font=ImageFont.truetype(font='江城圆体 600W.ttf',size=130) 
    # 第一帧
    #text=ImageDraw.Draw(bg)
    #text.multiline_text((843,565),content,anchor="mm",fill='#f8df70',font=font,spacing=100,align="center")
    #bg.save('1.tiff')
    return


'''
content="测试文字1"
# 生成一个白色底板
bg=Image.new("RGB",(3840,2160),(255,255,255)) 
bg.save('1.tiff')
'''

# 生成一年的时间字符串
def time_l():
    start_time='2023.01.01'
    time_l=[start_time]
    for i in range(365):
        time_t= datetime.strptime(start_time,"%Y.%m.%d")
        date=time_t+timedelta(days=1)
        start_time=datetime.strftime(date, "%Y.%m.%d")
        time_l.append(start_time)
    return time_l

# 生成一个下行的颜色序列
def color_scale():
    str_color_l=[]
    r,g,b,=95,55,55
    while 255 not in [r,g,b]:
        add=lambda x:x+5
        r,g,b=add(r),add(g),add(b)
        str_color="rgb(%s,%s,%s)"%(r,g,b)
        str_color_l.append(str_color)
    return str_color_l

str_color_l=color_scale()
str_color_l=str_color_l*1000
time_str=time_l()
for v1,v2 in zip(str_color_l,time_str):
    cover_t=create_cover.create_cover('江城圆体 400W',v1,'#FFFFFF',"节奏听辨\n%s"%v2,"节奏听辨\n%s"%v2)
    pic=cover_t.wechat()
    pic.save('rhythm/rhythm-%s.png'%v2)