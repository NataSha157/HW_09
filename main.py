# Парсимо всі сторінки сайта (через next) та всі сторінки авторів.
# На виході маємо 2 файла: authors.json та quotes.json
import json
import re

import requests
from bs4 import BeautifulSoup

from connect import bs4_url

base_url = bs4_url


def get_content(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    return soup


def get_quote(soup):
    quote_list = []
    quote = soup.find_all('span', class_='text')
    author = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')
    for i in range(len(quote)):
        t = tags[i].text.strip().split(':')
        if len(t) > 1:
            tt = t[1].strip().split('\n')
        else:
            tt = ['']
        res = {"tags": tt, "author": author[i].text,
               "quote": quote[i].text}
        quote_list.append(res)
    return quote_list


def get_author(url):
    soup = get_content(url)
    name = soup.find('h3', class_='author-title').text.strip()
    born_date = soup.find('span', class_='author-born-date').text.strip()
    born_place = soup.find('span', class_='author-born-location').text.strip()
    description = (soup.find('div', class_='author-description').text.strip()).replace("\'", "'")
    author_dict = {"fullname": name, "born_date": born_date, "born_location": born_place, "description": description}
    return author_dict



def get_author_urls(bace_url):
    urls = []
    html_doc = requests.get(bace_url)
    soup = BeautifulSoup(html_doc.text, 'html.parser')
    content_link = soup.select('div[class=quote] span a')
    for link in content_link:
        url = bs4_url + re.search(r"author/[\w-]+", str(link)).group()
        urls.append(url)
    return urls


def get_next(url):
    urls = [url]
    while True:
        html_doc = requests.get(url)
        soup = BeautifulSoup(html_doc.text, 'html.parser')
        next_link = soup.select('nav ul[class=pager] li[class=next] a')
        if next_link:
            url_next = bs4_url + re.search(r"page/\d+", str(next_link)).group()
            url = url_next
            urls.append(url)
        else:
            break
    return urls


def write_json(content, file_name):
    with open(file_name, 'w', encoding='utf-8') as fd:
        json.dump(content, fd, ensure_ascii=False, indent=2)


def main(base_url):
    list_next = get_next(base_url)
    list_author_links = []
    list_quote_all = []
    author_json = []
    for url in list_next:
        print(url)
        soup = get_content(url)
        author_links = get_author_urls(url)
        list_author_links += author_links
        quote_list = get_quote(soup)
        list_quote_all += quote_list
    set_author_links = set(list_author_links)
    for link in set_author_links:
        author_dict = get_author(link)
        author_json.append(author_dict)
    write_json(list_quote_all, 'quotes.json')
    write_json(author_json, 'authors.json')


if __name__ == '__main__':
    main(base_url)


