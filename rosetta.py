#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: loricheung
import os
import pickle
from fontTools import ttLib


class Rosetta(object):
    """点评字体反爬破解"""
    def __init__(self, num_font_file, char_font_file):
        """
        Paramters:

        """
        MAPPING_FILE = "character"
        self.num_font = ttLib.TTFont(num_font_file)
        self.char_font = ttLib.TTFont(char_font_file)
        self.table = pickle.load(open(os.path.join(os.path.curdir, MAPPING_FILE), "rb"))

    def _is_normal_char(self, char):
        if len(char) <= 1:
            if self._is_emoji(char):
                return True
            if ord(char) < 0x9FEF:
                return True
            else:
                char = char.encode("unicode_escape")
                if hex(int(char.replace(b"\\u", b"").decode(), 16)) < "0xe000":
                    return True
        else:
            if any([ord(c) < 0x9FEF for c in char]):
                return True

    def _is_emoji(self, content):
        if not content:
            return False
        elif u"\U0001F300" <= content and content <= u"\U0001F9EF":
            return True
        else:
            return False

    def _get_chinese_char(self, chr):
        uni_chr = (
            b"uni"
            + chr.replace(b" ", b"")
            .replace(b"\\n", b"")
            .replace(b"\\t", b"")
            .replace(b"\\u", b"")
        ).decode()
        try:
            char_index = self.char_font.getGlyphID(uni_chr)
        except Exception:
            char_index = 0

        try:
            num_index = self.num_font.getGlyphID(uni_chr)
        except Exception:
            num_index = 2**10

        index = num_index if (num_index & num_index < 12) else char_index
        return self.table[index - 2]

    def _convert(self, chr):
        if chr.isascii():
            return chr
        if self._is_normal_char(chr):
            return chr
        try:
            chr_b = (
                chr.encode("unicode_escape", errors="ignore")
                .replace(b" ", b"")
                .replace(b"\\n", b"")
                .replace(b"\\t", b"")
                .replace(b"\\xa0", b", ")
            )
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
        return "".join([str(c).strip() for c in chr_list])
