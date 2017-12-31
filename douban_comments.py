import pandas
import requests
from lxml import etree
# from bs4 import BeautifulSoup

r = requests.get('https://book.douban.com/subject/1084336/comments/')

# comments = []
# soup = BeautifulSoup(r.text, 'lxml')
# items = soup.find_all('p', 'comment-content')
# for i in items:
#     comments.append(i.string)
# df = pandas.DataFrame(comments)
# df.to_csv('comments.csv')

s = etree.HTML(r.text)
items = s.xpath('//div[@class="comment"]/p/text()')

with open('comments.txt', 'w', encoding='utf-8') as f:
    for i in items:
        f.write(i)

df = pandas.DataFrame(items)
df.to_excel('comments.xlsx')
