import json
import requests
import bs4
from fake_headers import Headers


keywords = ['дизайн', 'фото', 'web', 'python']
response = requests.get(url='https://habr.com/ru/articles/', headers=Headers(browser='chrome', os='win').generate())

soup = bs4.BeautifulSoup(response.text, features='lxml')
news_list = soup.select_one('div.tm-articles-list')
articles = news_list.select('div.tm-article-snippet')

parsed_data = []

for article in articles:
    link = article.select_one('a.tm-title__link')
    response = requests.get('https://habr.com' + link['href'])
    article_soup = bs4.BeautifulSoup(response.text, features='lxml')
    title = link.select_one('span').text
    body = article.find('div', class_='article-formatted-body')
    time = article_soup.select_one('time')['datetime']
    for i in keywords:
        if i.lower() in title.lower() or i.lower() in body.text.lower():

            parsed_data.append({
                'title': title,
                'time': time,
                'URL': 'https://habr.com' + link['href'],
            })

with open('articles.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(parsed_data, ensure_ascii=False, indent=3))
