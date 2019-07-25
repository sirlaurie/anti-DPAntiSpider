#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: loricheung

import sys
sys.path.append('..')
from svgdetect import Svgdetect, request_html

headers = {
    'Host': 'www.dianping.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.72 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://www.dianping.com/shop/17679013',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-US;q=0.7',
    'Cookie': 'cy=1; cye=shanghai; s_ViewType=10; _hc.v=f81e6399-b15a-e55d-8908-ad62708b389a.1562725845;cityid=1;switchcityflashtoast=1; source=m_browser_test_33; default_ab=shop%3AA%3A5%7Cindex%3AA%3A1%7CshopList%3AC%3A4;dper=f2d14c1f466f3ccb52036263ec24ac28e46f73539d53b823d02fe000507b544ce2fc41f68a9db34d57fc2fc3c1506110c1f19441c600038d3a28729835f85e495944f435f79c60cbf9a148436d1409f58eb2b074990267152b31369b8117761d; ll=7fd06e815b796be3df069dec7836c3df;ua=anguslg; ctu=bccc8a4462d5037c2663332c6e5dafb6263551d3a27e3f5d3168a2452e6a9971; uamo=17621346320'
}

html = request_html('http://www.dianping.com/shop/17679013/review_all', headers=headers)

text_list = ['review-words Hide',
             '\n                            薛',
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

s = Svgdetect(html)

print(s.parse(text_list))
