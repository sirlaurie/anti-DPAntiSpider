#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: loricheung

import sys
sys.path.append('..')
from rosetta import Rosetta, request_html, woff_file

# html = request_html()
# font_file = woff_file(html)
# rosetta = Rosetta('/path/to/file.woff')
rosetta = Rosetta('./num_font.woff', './char_font.woff')
chr_list = [' 肇', '\ue09c', '浜', '\ue163', '\ue1fc', '\ue585', '\ueca2', '\uecb3', '(', '\uf562', '\ue67c', '\ue860', '\ue53f', '\ue163', '，', '\uf6b5', '\ue3f0', '\ue9e3', '､1', '\uf0b9', '\uecb3', '\ue86d', '\ue09c', '善', '\ue163', '\uf68e', '\uf6e1', '\uecb3', '\uf88f', '\ue172', ') ']
print(rosetta.convert([c.strip() for c in chr_list]))
