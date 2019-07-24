#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: loricheung

import re
import time
import pickle
import requests
from fontTools import ttLib

css_pattern = re.compile(r'\/\/s3plus\.meituan\.net/v1/(.*?)\/svgtextcss/(.*?)\.css')
woff_pattern = re.compile(r'\/\/s3plus\.meituan\.net/v1/mss_\w+\/font\/\w+\.woff')


def count(func):
    def wrapper(*args, **kwargs):
        """
        可以检测是否遭到访问限制的装饰器
        :Parameters:
            url: url
            headers: headers
            query: query
            sleep: sleep time
        """
        times = 1
        while True:
            print(f'request {args[0]} for {times} time ...')
            resp_url, html = func(*args, **kwargs)
            if resp_url.strip('/') == args[0]:
                break
            times += 1
        return html
    return wrapper


@count
def request_html(url, headers=None, query=None, sleep=10):
    time.sleep(sleep)
    resp = requests.get(url, headers=headers, params=query)
    return resp.url, resp.content.decode()


def woff_file(html):
    """下载反爬需要的woff字体文件"""
    css = css_pattern.search(html)
    if css:
        css_url = css.group()
        css_content = request_html('http:' + css_url, headers=None, query=None, sleep=0)
        woff = woff_pattern.search(css_content)
        if woff:
            woff_url = woff.group()
            return download_file('http:' + woff_url)
        else:
            print('未能找到字体链接')
    else:
        print('未能找到css文件链接')


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return local_filename


class Rosetta(object):

    def __init__(self, font_file):
        """传入woff文件实例化, 调用 convert 方法转换加密字体"""
        MAPPING_FILE = './character'
        self.font = ttLib.TTFont(font_file)
        self.table = pickle.load(open(MAPPING_FILE, 'rb'))

    def _is_normal_char(self, char):
        if len(char) <= 1:
            if ord(char) < 0x9FEF:
                return True
            else:
                char = char.encode('unicode_escape')
                if hex(int(char.replace(b'\\u', b'').decode(), 16)) < '0xe000':
                    return True
        else:
            if any([ord(c) < 0x9FEF for c in char]):
                return True

    def _get_chinese_char(self, chr):
        uni_chr = (b'uni' + chr.replace(b' ', b'').replace(b'\\n', b'').replace(b'\\t', b'').replace(b'\\u', b'')).decode()
        index = self.font.getGlyphID(uni_chr)
        return self.table[index - 2]

    def _convert(self, chr):
        if chr.isascii():
            return chr
        if self._is_normal_char(chr):
            return chr
        try:
            chr_b = chr.encode('unicode_escape', errors='ignore').replace(b' ', b'').replace(b'\\n', b'').replace(b'\\t', b'').replace(b'\\xa0', b', ')
            return self._get_chinese_char(chr_b)
        except Exception:
            return chr

    def convert(self, chr_list):
        """
        :Parameters:
            chr_list: 网页上抓取的所有文字(包含未加密的)列表
        :Returns:
            str: 解密后的文字
        """
        chr_list = filter(lambda x: len(x.strip()) != 0, chr_list)
        chr_list = list(map(self._convert, [c.strip() for c in chr_list]))
        return ''.join([str(c).strip() for c in chr_list])
