#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @author: loricheung
import re
import time
import requests

css_pattern = re.compile(r'\/\/s3plus\.meituan\.net/v1/(.*?)\/svgtextcss/(.*?)\.css')
svg_pattern = re.compile(r'\/\/s3plus\.meituan\.net/v1/(.*?)\/svgtextcss/(.*?)\.svg')
woff_pattern = re.compile(r'\/\/s3plus\.meituan\.net/v1/mss_\w+\/font\/\w+\.woff')
refuse_visit = re.compile(r'抱歉！页面无法访问')


def count(func):
    def wrapper(*args, **kwargs):
        """可以检测是否遭到访问限制的装饰器.

        Parameters:
            url: url.
            headers: headers.
            query: query.
            sleep: sleep time.
        """
        times = 1
        while True:
            print(f'request {args[0]} for {times} time ...')
            resp_url, html = func(*args, **kwargs)
            if (resp_url.strip('/') == args[0] and not refuse_visit.search(html)):
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
    """下载文件"""
    css = css_pattern.search(html)
    if css:
        css_url = css.group()
        css_content = request_html('http:' + css_url, headers=None, query=None, sleep=0)
        woff = woff_pattern.search(css_content)
        if woff:
            woff_url = woff.group()
            return download_file('http:' + woff_url)
        else:
            print('Error: no woff font link found!')
            exit()
    else:
        print('Error: no css link found!')
        exit()


def download_file(url):
    local_filename = url.split('/')[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return local_filename
