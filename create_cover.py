from PIL import Image,ImageDraw,ImageFont

class create_cover:
    def __init__(self,font_file,bg_color,text_color,big_content,small_content):
        # 字体路径
        self.font_file=font_file
        # 正文文字颜色｜用rgb数值控制
        self.text_color=text_color
        # 背景颜色
        self.bg_color=bg_color
        # 正文内容
        self.big_content=big_content
        self.small_content=small_content
    def hexo(self):
        # 背景大小
        big_bg_size=(1686,1130)
        # 设定字体文件与大小
        font=ImageFont.truetype(font=self.font_file,size=130) 
        # ---------------------------------------
        # 大图
        big_bg=Image.new("RGB",big_bg_size,self.bg_color) 
        # 确定正文位置
        big_text=ImageDraw.Draw(big_bg)
        big_text.multiline_text((843,565),self.big_content,anchor="mm",fill=self.text_color,font=font,spacing=100,align="center")
        return big_bg
    def wechat(self):
        # 背景大小
        bg_size=(3350,1000)
        # ---------------------------------------
        # 设定字体文件与大小
        font=ImageFont.truetype(font=self.font_file,size=130) 
        # 生成一个背景
        background=Image.new("RGB",bg_size,self.bg_color) 
        # 左边的大图位置
        big=ImageDraw.Draw(background)
        big.multiline_text((1175,500),self.big_content,anchor="mm",fill=self.text_color,font=font,spacing=100,align="center")
        # 绘制右边的正方形
        right=ImageDraw.Draw(background)
        right.multiline_text((2850,400),self.small_content,anchor="mm",fill=self.text_color,font=font,spacing=60)
        return background
    def blog(self):
        # 背景大小
        big_bg_size=(2400,900)
        small_bg__size=(900,900)
        # 设定字体文件与大小
        font=ImageFont.truetype(font=self.font_file,size=130) 
        # ---------------------------------------
        # 大图
        big_bg=Image.new("RGB",big_bg_size,self.bg_color) 
        # 确定正文位置
        big_text=ImageDraw.Draw(big_bg)
        big_text.multiline_text((1200,450),self.big_content,anchor="mm",fill=self.text_color,font=font,spacing=100,align="center")
        # ---------------------------------------
        # 小图
        small_bg=Image.new("RGB",small_bg__size,self.bg_color) 
        # 确定正文位置
        small_text=ImageDraw.Draw(small_bg)
        small_text.multiline_text((450,450),self.small_content,anchor="mm",fill=self.text_color,font=font,spacing=100)
        return big_bg,small_bg
    def zhihu(self,zhihu_pre):
        # 定好线进行预览
        def show_line(pic):
            line_draw=ImageDraw.Draw(pic)
            line_xy=[(423,0),(423,840)]
            line_draw.line(line_xy,width=1)
            line_xy=[(1647,0),(1647,840)]
            line_draw.line(line_xy,width=1)
            return '绘制成功'
        # ---------------------------------------
        # 背景大小
        bg_size=(2070,840)
        # 设定字体文件与大小
        font=ImageFont.truetype(font=self.font_file,size=85) 
        # ---------------------------------------
        # 生成背景图
        background=Image.new("RGB",bg_size,self.bg_color) 
        # 确定正文位置
        text=ImageDraw.Draw(background)
        text.multiline_text((1035,420),self.big_content,anchor="mm",fill=self.text_color,font=font,spacing=100,align="center")
        # 送去预览
        if zhihu_pre==1:
            show_line(background) 
        return background