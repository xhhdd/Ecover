# -*- coding: utf-8 -*-

from pywebio.input import *
from pywebio.output import *
from pywebio import platform
from pywebio.pin import *
from pywebio.session import *


def main():
    @defer_call
    def cleanup():
        open('1.txt','wb').read(b'1')
    input('name',type=TEXT)
if __name__ == '__main__':
    platform.start_server(main,port=5012,debug=True)