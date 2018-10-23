#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytesseract
from PIL import Image
image = Image.open('piccode.png')
# 设置 tesseract 的安装路径
pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe'
code = pytesseract.image_to_string(image)
print(code)
