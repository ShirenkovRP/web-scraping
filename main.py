#  Необходимо парсить страницу со свежими статьями (вот эту) и выбирать те статьи,
#  в которых встречается хотя бы одно из ключевых слов (эти слова определяем в начале скрипта).
#  Поиск вести по всей доступной preview-информации (это информация, доступная непосредственно с текущей страницы).
#  Вывести в консоль список подходящих статей в формате: <дата> - <заголовок> - <ссылка>.
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests


def datetime_today(arg):
    if "сегодня" in arg:
        when = datetime.date(datetime.today())
        return f"{when} в {arg[10:]}"
    if "вчера" in arg:
        when = datetime.date(datetime.today()) - timedelta(1)
        return f"{when} в {arg[8:]}"
    else:
        return arg


def response(arg):
    resp_d = requests.get(arg)
    if resp_d.status_code != 200:
        raise Exception("Ошибка запроса")
    return resp_d


def post_preview(arg):
    post_preview_list = []
    title = arg.find("a", {"class": "post__title_link"})
    when = arg.find("span", {"class": "post__time"}).text
    post_preview_list.append(datetime_today(when))
    post_preview_list.append(title.text)
    post_preview_list.append(title["href"])
    return post_preview_list


def relevant_articles(arg, arg_2):
    if any(kw in arg.text for kw in arg_2):
        return arg


def text_search(arg, arg_2):
    url = arg.find("a", {"class": "btn btn_x-large btn_outline_blue post__habracut-btn"}).attrs.get("href")
    resp_d = response(url).text
    bs = BeautifulSoup(resp_d, features="html.parser")
    article_text = bs.find("div", {"id": "post-content-body"}).get_text()
    if any(kw in article_text for kw in arg_2):
        return arg


#  определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

resp = response("https://habr.com/ru/all").text
soup = BeautifulSoup(resp, features="html.parser")
articles = soup.find_all("article", {"class": "post post_preview"})

#  поиск статей по ключевым словам
print("Список статей содержащих ключевые слова")
for article in articles:
    relevant = relevant_articles(article, KEYWORDS)
    relevant_2 = text_search(article, KEYWORDS)
    if relevant is not None:  # поиск статей по ключевым словам в preview-информации
        print(post_preview(relevant))
    elif relevant_2 is not None:  # поиск статей по ключевым словам в тексте статьи
        print(post_preview(relevant_2))
