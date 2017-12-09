#!usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq


class QSBK(object):

    def __init__(self):
        self.enable = False
        self.page = 1
        self.stories = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }

    def download(self, url):
        r = requests.get(url, headers=self.headers)
        return r

    def parse(self, url):
        r = self.download(url)
        d = pq(r.text)
        qs_tags = d('#content-left').children('div')
        page_stories = []
        for i in range(25):
            qs_i = qs_tags.eq(i)
            has_img = qs_i('div').has_class('thumb')
            if has_img is False:
                author = qs_i('h2').text()
                content = qs_i('.content').find('span').text()
                number = qs_i('i').filter('.number').eq(0).text()
                story = (author.strip(), number.strip(), content.strip())
                page_stories.append(story)
        return page_stories

    def manage(self):
        if self.enable is True:
            if len(self.stories) < 2:
                url = 'https://www.qiushibaike.com/hot/page/' + str(self.page)
                page_stories = self.parse(url)
                self.stories.append(page_stories)
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
