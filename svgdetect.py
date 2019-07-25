#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: loricheung
import re
from parsel import Selector
from util import request_html, css_pattern, svg_pattern


class Svgdetect(object):
    """一个可以转换点评svg文字为正常文字的脚本. 调用 parse 方法, 传入待转换的文字列表即可"""

    def __init__(self, html):
        """
          Parameters:
            html: 网页的文本文档, response.content.decode()
        """
        self.html = html
        self._sel = Selector(html)
        self._css_svg()

    def _css_svg(self):
        css = css_pattern.search(self.html)
        if css:
            css_url = css.group()
            self._css_content = request_html('http:' + css_url, sleep=0)
            self.class_prefix = self._sel.xpath('//svgmtsi/@class').get()[:2]
            svg_url = re.search(r'svgmtsi.*?url\((.*?)\)', self._css_content).group(1)
            if (svg_url.startswith('//s3plus') and svg_url.endswith('.svg')):
                svg_content = request_html('http:' + svg_url)
                self._svg_sel = Selector(svg_content)
            else:
                print('Error: No svg link found!')
                exit()
        else:
            print('Error: No css link found!')
            exit()

    def _svg_a(self):
        shift_list = list(map(int, self._svg_sel.xpath('//text[@x="0"]/@y').getall()))
        return shift_list

    def _svg_b(self):
        shift_list = list(map(int, [x.split()[1] for x in self._svg_sel.xpath('//path[starts-with(@d, "M0")]/@d').getall()]))
        return shift_list

    def _find_in_svg(self, char):
        if char.isascii():
            loc = re.search(char + r'{background:(.*?);}', self._css_content).group(1)
            loc = list(map(abs, [float(x.strip('px')) for x in loc.split()]))
            index = int(loc[0] / 14)

            shift_list = self._svg_a() or self._svg_b()
            row_index = shift_list.index(min(list(filter(lambda x: x > int(loc[1]), shift_list))))

            text_str = self._svg_sel.xpath(f'//svg//text[{row_index + 1}]/text() | //svg//textpath[{row_index + 1}]/text()').getall()

            return ''.join(text_str).strip()[index] or char
        else:
            return char

    def _clean(self, lst):
        lst = map(lambda x: x.strip(), lst)
        lst = filter(lambda x: len(x) != 0, lst)
        lst = list(filter(lambda x: x.startswith(self.class_prefix) if x.isascii() else x, lst))
        return lst[:-1]

    def parse(self, char_list):
        """解析svg图形文字
          Parameters:
            char_list: 包含正常文字和svg文字的class属性的列表, 形如
                ['review-words Hide',
                 '\n     薛',
                 'ul8s9',
                 '谦',
                 'ul8sk',
                 '火锅店，',
                 'ullxx',
                 '就',
                 'ulxtf',
                 '仰大名了，',
                 'ulejv',
                 '着',
                 'ulgj8',
                 'ul9he',
                 '事聚',
                 'uli7t',
                 '，过',
                 'uls4f',
                 '种种草。']
          Returns:
            str: 解密后的文字
        """
        char_list = self._clean(char_list)
        return ''.join(map(self._find_in_svg, char_list))
