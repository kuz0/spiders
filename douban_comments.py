import pandas
import requests
from bs4 import BeautifulSoup
from lxml import etree

comments = []
r = requests.get('https://book.douban.com/subject/1084336/comments/')

# soup = BeautifulSoup(r.text, 'lxml')
# items = soup.find_all('p', 'comment-content')
# for i in items:
#     comments.append(i.string)
#     print(i.string)

s = etree.HTML(r.text)
items = s.xpath('//div[@class="comment"]/p/text()')
for i in items:
    comments.append(i)
    print(i)

df = pandas.DataFrame(comments)
df.to_csv('comments.csv')
