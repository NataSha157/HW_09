# завантаження даних у хмарну БД напряму з .json файлів (від викладача)
import json

from mongoengine.errors import NotUniqueError

from models import Author1, Quote1

if __name__ == '__main__':
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author1(fullname=el.get('fullname'), born_date=el.get('born_date'),
                                born_location=el.get('born_location'), description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"The author {el.get('fullname')} already exists")

    with open('quotes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        n=0
        for el in data:
            author, *_ = Author1.objects(fullname=el.get('author'))
            print(n, author.fullname)
            n+=1
            quote = Quote1(quote=el.get('quote'), tags=el.get('tags'), author=author)
            print(el.get('tags'))
            quote.save()