# скрипт для пошуку цитат за тегом, за ім'ям автора або набором тегів
from models import Author1, Quote1

count = 0


def find_author(author):
    author_quote = Author1.objects(fullname=author).first()
    if author_quote:
        return Quote1.objects(author=author_quote).all()
    else:
        print('We have not this author')


def find_teg(tag):
    res = Quote1.objects(tags=tag).all()
    if res:
        return res
    else:
        print('A quote wis this tag does not exist')
        return None


def find_tegs(tags):  # Не вийшло зробити універсальний return, тому друк у функції
    tags_list = tags.split(',')
    # res = Quote.objects(tags=(t for t in tags_list)).all() # Not doing
    for tag in tags_list:
        res = Quote1.objects(tags=tag.strip()).all()
        if res:
            for i in res:
                print(i.quote, i.author.fullname)
        else:
            print(f'A quote with tag "{tag}" does not exist')


while True:
    act = input("Please, enter your request according to the following options: \n"
                "search for quotes by author name: 'a:fullname' \n"
                "search for quotes by one teg: 't:teg' \n"
                "search for quotes by some tegs: 'ts:teg,teg,... \n"
                "or enter 'exit' \n")
    if act == "exit":
        print(f'You did {count} requests')
        break
    else:
        r = None
        count += 1
        a = act.split(':')
        a_1 = a[1].strip()
        if a[0].strip() == 'a':
            r = find_author(a_1)
        elif a[0].strip() == 't':
            r = find_teg(a[1].strip())

        elif a[0].strip() == 'ts':
            find_tegs(a[1].strip())
        else:
            print("It's unknown command")
            print(f'You did {count} requests')
            continue
        if r == None:
            continue
        else:
            for i in r:
                print(i.quote, i.author.fullname)
            print(count, ' request')
