import pandas
import requests
from bs4 import BeautifulSoup

r = requests.get('https://book.douban.com/subject/1084336/comments/')

soup = BeautifulSoup(r.text, 'lxml')
items = soup.find_all('p', 'comment-content')
for i in items:
    print(i.string, '\n')

comments = []
for i in items:
    comments.append(i.string)
df = pandas.DataFrame(comments)
df.to_csv('comments.csv')
