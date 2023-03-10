# -*- coding: utf-8 -*-
from pywebio.input import *
from pywebio.output import *
from pywebio import platform
from pywebio.pin import *
from pywebio.session import *
from pywebio import config
# 其他模块
import time
import os
# 其他模块
from create_color import *
from create_cover import *

config(title='封面图生成',
       description='简单生成各平台的封面图',
       theme='minty'
       )


def main():
    image_url = "https://cdn.xhhdd.cc/uPic2/2ZUaT3.png"
    run_js("""
    $('#favicon32,#favicon16').remove(); 
    $('head').append('<link rel="icon" type="image/png" href="%s">')
    """ % image_url)

    # 最上方一直保持显示的进度提示
    def intro():
        with use_scope('intro'):
            put_markdown(r""" # 输入字体、颜色等信息生成封面图
            """)
        put_processbar('process', init=0)
        return

    intro()

    # 选择字体————————————————————————————
    def font():
        font_mode = actions(label='选择字体', buttons=['选择默认字体', '上传字体文件'])
        set_processbar('process', 2 / 10)
        if font_mode == '上传字体文件':
            with use_scope('normal_top_s', clear=True):
                save_file = file_upload('上传字体',
                                        accept=['.ttf', '.ttc', '.otf'],
                                        placeholder='支持ttf、ttc、otf格式',
                                        max_size='100m',
                                        required=True
                                        )
                split_l = save_file['filename'].split('.', -1)
                file_path = 'temp_file/' + str(int(time.time())) + '.' + split_l[-1]
                open(file_path, 'wb').write(save_file['content'])
                font_result = file_path[:]

                # 清理文件
                @defer_call
                def cleanup():
                    os.remove(font_result)
        if font_mode == '选择默认字体':
            with use_scope('normal_top_s', clear=True):
                choice_font = select(
                    '选择封面图上的字体',
                    options=['思源黑体_Regular',
                             '霞鹜文楷GB_Light',
                             '霞鹜文楷GB_Regular',
                             '霞鹜文楷GB_Bold',
                             '霞鹜文楷GB-mono_Light',
                             '霞鹜文楷GB-mono_Regular',
                             '霞鹜文楷GB-mono_Bold',
                             '阿里巴巴普惠体_Light',
                             '阿里巴巴普惠体_Regular',
                             '阿里巴巴普惠体_Medium',
                             '阿里巴巴普惠体_Bold',
                             '阿里巴巴普惠体_Heavy',
                             '江城圆体 300W',
                             '江城圆体 400W',
                             '江城圆体 500W',
                             '江城圆体 600W',
                             '江城圆体 700W'
                             ]
                )
                font_result = choice_font

        return font_result

    font_result = font()
    font_result_s = font_result[:]  # 数值存储

    # 选择颜色模式————————————————————————————
    def color_mode():
        with use_scope('normal_top_s', clear=True):
            put_markdown(r""" # 选择颜色
            - **颜色方案1**会随机决定背景与文字的颜色。
            - **颜色方案2**背景颜色随机，文字都是白色。
            """)
        choice_color_mode = radio(
            options=['自定义颜色', '随机颜色方案1', '随机颜色方案2'],
            label='选择颜色方案',
            required=True
        )
        set_processbar('process', 3 / 10)
        return choice_color_mode

    choice_color_mode = color_mode()
    color_mode_s = choice_color_mode[:]  # 内容存储

    # 输出具体颜色数值————————————————————————————
    def color_value(choice_color_mode):
        if choice_color_mode == '自定义颜色':
            bg_text_clor = input_group("选择颜色", [
                input('背景颜色', name='bg_color', type=COLOR),
                input('文字颜色', name='text_color', type=COLOR)
            ])
            bg_color, text_color = bg_text_clor['bg_color'], bg_text_clor['text_color']
        elif choice_color_mode == '随机颜色方案1':
            bg_color, text_color = random_color_mode_1()
        else:
            bg_color, text_color = random_color_mode_2()
        set_processbar('process', 6 / 10)
        return bg_color, text_color

    bg_color, text_color = color_value(color_mode_s)
    bg_color_s, text_color_s = bg_color[:], text_color[:]  # 内容存储

    # 选择生成的平台及模式————————————————————————————
    def platform():
        with use_scope('normal_top_s', clear=True):
            put_markdown(r""" # 选择对应的平台
            目前支持四个平台的封面图生成，
            其中handsome主题是在typecho博客系统上的一个付费主题。
            hexo是根据NotionNext来的，我也不知道真的比例是多少，知道的小伙伴可以告诉我。
            """)
        choice_platform = radio(
            options=['微信公众号', '知乎', 'hexo', 'handsome主题的blog', 'bilibili',
                     '正方形'],
            label='选择对应的平台',
            required=True,
            help_text='不同的平台对应不同的生成策略'
        )
        set_processbar('process', 7 / 10)
        return choice_platform

    choice_platform = platform()
    choice_platform_s = choice_platform[:]  # 内容存储

    # 输入文字信息————————————————————————————
    def content(choice_platform):
        with use_scope('normal_top_s', clear=True):
            put_markdown(r""" # 输入文字内容
            - 大图每一行字数建议为
            - 小图每一行字数建议为
            """)
        # 决定输入文字的行数
        if choice_platform in ['知乎', 'hexo', 'bilibili', '正方形']:
            big_content = textarea('封面图内容', rows=4, type=TEXT, required=True)
            big_content, small_content = big_content, ''
        if choice_platform in ['微信公众号', 'handsome主题的blog']:
            big_small_content = input_group("输入封面图文字", [
                textarea('大图文字', name='big_content', rows=4, type=TEXT, required=True),
                textarea('小图文字', name='small_content', rows=4, type=TEXT, required=True)]
                                            )
            big_content, small_content = big_small_content['big_content'], big_small_content['small_content']
        # 进度条
        set_processbar('process', 8 / 10)
        return big_content, small_content

    big_content, small_content = content(choice_platform_s)
    big_content_s, small_content_s = big_content[:], small_content[:]  # 内容存储

    # 生成一个demo————————————————————————————
    def creat_cover_demo(choice_platform, font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s):
        # 进度条
        set_processbar('process', 9 / 10)

        def save_pic(pic_l: Image, user_name):
            for v in pic_l:
                file_time = str(int(time.time())) + '.png'
                v.save(file_time)
                content = open(file_time, 'rb').read()
                download(user_name, content)
                toast('下载成功', color='#2188ff', duration=1)
                os.remove(file_time)
                set_processbar('process', 10 / 10)
            return

            # 微信————————————————————————————

        if choice_platform == '微信公众号':
            pic = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).wechat()
            with use_scope('normal_top_s', clear=True):
                put_markdown(r""" # 图片介绍
                微信公众号发布文章的时候，可以指定一张图。
                但大头图跟小头图都是根据这一张图进行裁剪，
                并不能选择两张单独的图。
                所以本函数就生成一张大图，左边适应大头图，右边适应小头图。
                - 这样发布公众号文章时，把图片选择框拉拽到最左边就会使用大头图，拉拽到最右边就会使用小头图。
                - 左边小头图文字起始位置会高一点，这是因为避免微信自动的水印遮盖文字。
                """)
            with use_scope('pic_demo', clear=True):
                put_markdown(r'''# 图片预览
                ''')
                with use_scope('pic_self', clear=True):
                    put_column([
                        put_image(pic, format='png'),
                        None,
                        put_button("点击下载", onclick=lambda: save_pic([pic], 'wechat.png'), color='danger')
                    ],
                        size='80% 10px 20%'
                    )

       # handsome————————————————————————————
        if choice_platform == 'handsome主题的blog':
            big, small = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).blog()
            with use_scope('normal_top_s', clear=True):
                put_markdown(r""" # 图片介绍 
                该函数主要是为了适应handsome这个博客主题。
                handsome可以同时填入大头图与小头图的链接，
                大头图是3比8的比例，小头图则是1比1正方形。
                所以本函数最终会生成两张图片。
                """)
            with use_scope('pic_demo', clear=True):
                put_markdown(r'''# 图片预览
                ''')
                put_column(
                    [
                        put_row(
                            [
                                put_column([put_markdown(r'''## 小头图
                                '''), put_image(small, format='png')], size='auto'),
                                None,
                                put_column([put_markdown(r'''## 大头图
                                '''), put_image(big, format='png')], size='auto')
                            ], size='30% 10px 70%'
                        ),
                        None,
                        put_button("点击下载", onclick=lambda: save_pic([big, small], 'handsome.png'), color='danger')
                    ], size='6fr 0.5fr 1fr'
                )

        if choice_platform == '知乎':
            def pre_save():
                pic = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).zhihu(
                    zhihu_pre=0)
                save_pic([pic], 'zhihu.png')
                return

            with use_scope('normal_top_s', clear=True):
                put_markdown(r""" # 图片介绍 
                知乎的事相对来说比较多。
                首先只能选择一张图片作为封面图，
                而且是自动裁剪。
                电脑上与手机上看到的效果也不一样的。
                ----------------
                所以在生成图片之前，先预览字有没有超过线。
                确认完毕之后再按下按钮进行生成。
                """)
            pre_pic = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).zhihu(
                zhihu_pre=1)
            with use_scope('pic_demo', clear=True):
                put_markdown(r'''# 图片预览
                ''')
                with use_scope('pic_self', clear=True):
                    put_column([
                        put_image(pre_pic, format='png'),
                        None,
                        put_button("确认未过线，点击下载", onclick=lambda: pre_save(), color='danger')
                    ],
                        size='6fr 0.5fr 1fr'
                    )

        if choice_platform == 'hexo':
            with use_scope('normal_top_s', clear=True):
                put_markdown(r""" # 图片介绍 
                最近在使用NotionNext这个项目，
                使用的是里面hexo这个主题，
                但是我对hexo并不了解，自己截图测量的比例...
                """)
            pic = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).hexo()
            with use_scope('pic_demo', clear=True):
                put_markdown(r'''# 图片预览
                ''')
                with use_scope('pic_self', clear=True):
                    put_column([
                        put_image(pic, format='png', width='50%'),
                        None,
                        put_button("点击下载", onclick=lambda: save_pic([pic], 'hexo.png'), color='danger')
                    ], size='6fr 0.5fr 1fr'
                    )

        if choice_platform == 'bilibili':
            with use_scope('normal_top_s', clear=True):
                put_markdown(r""" # 图片介绍 
                主要是上传b站视频的时候使用
                """)
            pic = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).bilibili()
            with use_scope('pic_demo', clear=True):
                put_markdown(r'''# 图片预览
                ''')
                with use_scope('pic_self', clear=True):
                    put_column([
                        put_image(pic, format='png', width='50%'),
                        None,
                        put_button("点击下载", onclick=lambda: save_pic([pic], 'bilibili.png'), color='danger')
                    ], size='6fr 0.5fr 1fr'
                    )

        if choice_platform == '正方形':
            with use_scope('normal_top_s', clear=True):
                put_markdown(r""" # 图片介绍 
                生成一张正方形的图片
                """)
            pic = create_cover(font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s).square()
            with use_scope('pic_demo', clear=True):
                put_markdown(r'''# 图片预览
                ''')
                with use_scope('pic_self', clear=True):
                    put_column([
                        put_image(pic, format='png', width='50%'),
                        None,
                        put_button("点击下载", onclick=lambda: save_pic([pic], 'square.png'), color='danger')
                    ], size='6fr 0.5fr 1fr'
                    )
    creat_cover_demo(choice_platform_s, font_result_s, bg_color_s, text_color_s, big_content_s, small_content_s)

    set_list = [bg_color_s, text_color_s, big_content_s, small_content_s, font_result_s]

    def re_create(mode):
        if mode == 'color':
            # 根据原有的颜色模式，重新获取颜色参数
            bg_color, text_color = color_value(color_mode_s)
            set_list[0], set_list[1] = bg_color, text_color
        # 存储新文字
        if mode == 'content':
            # 要求重新填写内容
            big_content, small_content = content(choice_platform_s)
            set_list[2], set_list[3] = big_content, small_content

        creat_cover_demo(choice_platform_s, set_list[4], set_list[0], set_list[1], set_list[2], set_list[3])
        return set_list

    with use_scope('re_creat'):
        put_markdown(r'''## 生成结果不满意？
        ''')
        put_row(
            [put_button('重新生成颜色', onclick=lambda: re_create('color'), color='primary'),
             put_button('重新填写文字', onclick=lambda: re_create('content'), color='secondary')]
        )


if __name__ == '__main__':
    # platform.path_deploy_http('/Users/xhhdd/Desktop/simple_platform_cover',port=5012,debug=True)
    platform.start_server(main, port=80, debug=True)
    # platform.tornado_http.start_server(main,port=5012,debug=True)
    # platform.path_deploy('/Users/xhhdd/Desktop/simple_platform_cover',port=5012,debug=True)
