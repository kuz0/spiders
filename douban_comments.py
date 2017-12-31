import pandas
import requests
from lxml import etree

url_format = 'https://book.douban.com/subject/1084336/comments/hot?p={}'
urls = [url_format.format(str(i)) for i in range(1, 6, 1)]

comments = []
for url in urls:
    r = requests.get(url)
    s = etree.HTML(r.text)
    items = s.xpath('//div[@class="comment"]/p/text()')
    comments += items

df = pandas.DataFrame(comments)
df.to_excel('comments.xlsx')
