#!usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from pyquery import PyQuery as pq

stories = []
url = 'https://www.qiushibaike.com/hot/page/1'
headers = {
     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0'
}
r = requests.get(url, headers=headers)
d = pq(r.text)
qs_tags = d('#content-left').children('div')
print(len(qs_tags))

for i in range(25):
    qs_i = qs_tags.eq(i)
    has_img = qs_i('div').has_class('thumb')
    if has_img is False:
        author = qs_i('h2').text()
        content = qs_i('.content').find('span').text()
        number = qs_i('i').filter('.number').eq(0).text()
        story = (author, content, number)
        stories.append(story)

print(len(stories))
for it in stories:
    print('\n发布人:{}\t赞:{}\n{}'.format(it[0], it[2], it[1]))