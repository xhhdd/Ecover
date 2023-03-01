from PIL import Image, ImageDraw, ImageFont


# 处理字体
def adjust_font(font_result):
    font_dict = {
        '思源黑体_Regular': 'SourceHanSansCN-Regular.otf',
        '霞鹜文楷GB_Light': 'LXGWWenKaiGBFusion-Light.ttf',
        '霞鹜文楷GB_Regular': 'LXGWWenKaiGBFusion-Regular.ttf',
        '霞鹜文楷GB_Bold': 'LXGWWenKaiGBFusion-Bold.ttf',
        '霞鹜文楷GB-mono_Light': 'LXGWWenKaiMonoGBFusion-Light.ttf',
        '霞鹜文楷GB-mono_Regular': 'LXGWWenKaiMonoGBFusion-Regular.ttf',
        '霞鹜文楷GB-mono_Bold': 'LXGWWenKaiMonoGBFusion-Bold.ttf',
        '阿里巴巴普惠体_Light': 'Alibaba-PuHuiTi-Light.ttf',
        '阿里巴巴普惠体_Regular': 'Alibaba-PuHuiTi-Regular.ttf',
        '阿里巴巴普惠体_Medium': 'Alibaba-PuHuiTi-Medium.ttf',
        '阿里巴巴普惠体_Bold': 'Alibaba-PuHuiTi-Bold.ttf',
        '阿里巴巴普惠体_Heavy': 'Alibaba-PuHuiTi-Heavy.ttf',
        '江城圆体 300W': '江城圆体 300W.ttf',
        '江城圆体 400W': '江城圆体 400W.ttf',
        '江城圆体 500W': '江城圆体 500W.ttf',
        '江城圆体 600W': '江城圆体 600W.ttf',
        '江城圆体 700W': '江城圆体 700W.ttf',

    }
    # 检测输入的是路径还是字体文件
    if font_dict.get(font_result) == None:
        font_file = font_result
    else:
        font_file = 'font_file/' + font_dict.get(font_result)
    return font_file


class create_cover:
    def __init__(self, font_result, bg_color, text_color, big_content, small_content):
        # 字体路径
        self.font_file = adjust_font(font_result)
        # 正文文字颜色｜用rgb数值控制
        self.text_color = text_color
        # 背景颜色
        self.bg_color = bg_color
        # 正文内容
        self.big_content = big_content
        self.small_content = small_content

    def hexo(self):
        # 背景大小
        big_bg_size = (1686, 1130)
        # 设定字体文件与大小
        font = ImageFont.truetype(font=self.font_file, size=130)
        # ---------------------------------------
        # 大图
        big_bg = Image.new("RGB", big_bg_size, self.bg_color)
        # 确定正文位置
        big_text = ImageDraw.Draw(big_bg)
        big_text.multiline_text((843, 565), self.big_content, anchor="mm", fill=self.text_color, font=font, spacing=100,
                                align="center")
        return big_bg

    def wechat(self):
        # 背景大小
        bg_size = (3350, 1000)
        # ---------------------------------------
        # 设定字体文件与大小
        font = ImageFont.truetype(font=self.font_file, size=130)
        # 生成一个背景
        background = Image.new("RGB", bg_size, self.bg_color)
        # 左边的大图位置
        big = ImageDraw.Draw(background)
        big.multiline_text((1175, 500), self.big_content, anchor="mm", fill=self.text_color, font=font, spacing=100,
                           align="center")
        # 绘制右边的正方形
        right = ImageDraw.Draw(background)
        right.multiline_text((2850, 400), self.small_content, anchor="mm", fill=self.text_color, font=font, spacing=60)
        return background

    def blog(self):
        # 背景大小
        big_bg_size = (2400, 900)
        small_bg__size = (900, 900)
        # 设定字体文件与大小
        font = ImageFont.truetype(font=self.font_file, size=130)
        # ---------------------------------------
        # 大图
        big_bg = Image.new("RGB", big_bg_size, self.bg_color)
        # 确定正文位置
        big_text = ImageDraw.Draw(big_bg)
        big_text.multiline_text((1200, 450), self.big_content, anchor="mm", fill=self.text_color, font=font,
                                spacing=100, align="center")
        # ---------------------------------------
        # 小图
        small_bg = Image.new("RGB", small_bg__size, self.bg_color)
        # 确定正文位置
        small_text = ImageDraw.Draw(small_bg)
        small_text.multiline_text((450, 450), self.small_content, anchor="mm", fill=self.text_color, font=font,
                                  spacing=100)
        return big_bg, small_bg

    def zhihu(self, zhihu_pre):
        # 定好线进行预览
        def show_line(pic):
            line_draw = ImageDraw.Draw(pic)
            line_xy = [(423, 0), (423, 840)]
            line_draw.line(line_xy, width=1)
            line_xy = [(1647, 0), (1647, 840)]
            line_draw.line(line_xy, width=1)
            return '绘制成功'

        # ---------------------------------------
        # 背景大小
        bg_size = (2070, 840)
        # 设定字体文件与大小
        font = ImageFont.truetype(font=self.font_file, size=85)
        # ---------------------------------------
        # 生成背景图
        background = Image.new("RGB", bg_size, self.bg_color)
        # 确定正文位置
        text = ImageDraw.Draw(background)
        text.multiline_text((1035, 420), self.big_content, anchor="mm", fill=self.text_color, font=font, spacing=100,
                            align="center")
        # 送去预览
        if zhihu_pre == 1:
            show_line(background)
        return background

    def bilibili(self):
        # 背景大小
        big_bg_size = (3456, 2160)
        # 设定字体文件与大小
        font = ImageFont.truetype(font=self.font_file, size=300)
        # ---------------------------------------
        # 大图
        big_bg = Image.new("RGB", big_bg_size, self.bg_color)
        # 确定正文位置
        big_text = ImageDraw.Draw(big_bg)
        big_text.multiline_text((1728, 1080), self.big_content, anchor="mm", fill=self.text_color, font=font,
                                spacing=100,
                                align="center")
        return big_bg

    def square(self):
        # 背景大小
        big_bg_size = (1920, 1920)
        # 设定字体文件与大小
        font = ImageFont.truetype(font=self.font_file, size=200)
        # ---------------------------------------
        # 大图
        big_bg = Image.new("RGB", big_bg_size, self.bg_color)
        # 确定正文位置
        big_text = ImageDraw.Draw(big_bg)
        big_text.multiline_text((960, 960), self.big_content, anchor="mm", fill=self.text_color, font=font, spacing=100
                                )
        return big_bg
