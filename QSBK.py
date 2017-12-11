#!usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq


class QSBK(object):

    def __init__(self):  # 初始化
        self.enable = False  # 控制程序启动和关闭的变量
        self.page = 1
        self.stories = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }

    def download(self, url):
        r = requests.get(url, headers=self.headers)
        return r

    def parse(self, url):  # 使用pyquery解析
        r = self.download(url)
        d = pq(r.text)
        qs_tags = d('#content-left').children('div')  # 找id='content-left'的标签及其子div标签
        page_stories = []
        for i in range(25):
            qs_i = qs_tags.eq(i)  # eq(i), 选取第i个标签
            has_img = qs_i('div').has_class('thumb')  # 找div标签,判断是否有'thumb'类,得到一个布尔值
            if has_img is False:
                author = qs_i('h2').text()  # 找h2标签,得到文本内容
                content = qs_i('.content').find('span').text()  # 找'content'类标签及其子孙span标签,得到文本内容
                number = qs_i('i').filter('.number').eq(0).text()  # 找i标签,并过滤得到有'number'类的,eq(0),选第一个
                story = (author.strip(), number.strip(), content.strip())  # .strip(),移除字符串首尾制定字符
                page_stories.append(story)
        return page_stories  # 返回含有整页故事的列表

    def manage(self):
        if self.enable is True:
            if len(self.stories) < 2:
                url = 'https://www.qiushibaike.com/hot/page/' + str(self.page)  # 构造url
                page_stories = self.parse(url)  # 解析url
                self.stories.append(page_stories)  # 将含有整页故事的对象传入self.stories变量中
                self.page += 1

    def get_one(self, page_stories, count):
        for s in page_stories:
            in_put = input('\n按回车查看新段子, Q退出\n')
            self.manage()
            if in_put == 'Q':
                self.enable = False
                return None
            print('第{}页\n发布人:{}\t赞:{}\n{}'.format(count, s[0], s[1], s[2]))

    def crawl(self):
        print('正在读取糗事百科')
        self.enable = True
        self.manage()
        count = 0
        while self.enable is True:
            if len(self.stories) > 0:
                page_stories = self.stories[0]
                count += 1
                del self.stories[0]
                self.get_one(page_stories, count)


if __name__ == '__main__':
    qs_bk = QSBK()
    qs_bk.crawl()
