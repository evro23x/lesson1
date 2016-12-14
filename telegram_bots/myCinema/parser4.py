from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

# получаем контент страницы
html_doc = urlopen('https://www.afisha.ru/msk/cinema/').read()
soup = BeautifulSoup(html_doc, "lxml")

# парсим список станци метро для получения привязки к ним кт
for li in soup.find('ul', {'class': 'b-dropdown-common-fixed'}).findAll('li'):
    # ссылка на метро формата - //www.afisha.ru/msk/cinema/cinema_list/aviamotornaya/
    # print(li.find('a')['href'])
    # название метро - Авиамоторная
    print("Станция метро: {}".format(li.find('a').contents[0]))
    # link_to_metro = li.find('a')['href']
    metro_to_cinema = BeautifulSoup(urlopen('https:' + li.find('a')['href']).read(), 'lxml')
    # парсим страницу с указанием привязки кт к станции метро
    for div_cinema in metro_to_cinema.find('div', {'class': 'b-places-list'}).findAll('h3'):
        # https://www.afisha.ru/msk/schedule_cinema_place/3652/
        # ссылка на кт формата - //www.afisha.ru/msk/cinema/34317/
        # print(div_cinema.find('a')['href'])
        # название кт - Летний кт на ВДНХ
        print("")
        print("Название кинотеатра: {}".format(div_cinema.find('a').contents[0]))

        # собираем правильную ссылку на рассписание кт с учетом его id
        pattern_url_table = 'https://www.afisha.ru/msk/schedule_cinema_place/'
        url_cinema = div_cinema.find('a')['href']
        id_cinema = url_cinema[url_cinema[0:-1].rfind('/') + 1:-1]
        url_table = pattern_url_table + id_cinema + '/'
        link_to_cinema = BeautifulSoup(urlopen(url_table).read(), 'lxml')

        # загружаем только два кт чтобы не тратить время
        # if div_cinema.find('a').contents[0] == "Спутник":
        #     exit(0)

        # проверка необходима чтобы парсер на валился на 3D фильмах
        try:
            # парсим фильмы и сеансы со страницы определенного кт
            for div_film in link_to_cinema.find('div', {'class': 'b-theme-schedule'}).findAll('tr'):
                # собираем сеансы в один список для удобство отображения в терминале
                session_list = []
                # print("==================================================================== start")
                for session in div_film.find('div', {'class': 'time-inside line'}).findAll('span'):
                    session_clear = ' '.join(session.contents[0].replace(' ', '').split())
                    # костылим и хардкодим, у сеанса есть три состояния, разберем по порядку
                    # 1 - сеанс прошел и на него нельзя купить билеты
                    # 2 - сеанс будет но на него нельзя купить билеты
                    # 3 - сеанс будет  и на него можно  купить билеты
                    if str(session).find("inactive") == 13:
                        session_list.append(session_clear)
                    elif str(session).find("href") == 10:
                        session_list.append(session.find("a").contents[0])
                    else:
                        session_list.append(session_clear)
                if str(div_film.find('span', {'class': 'title'})).find("Сеансы в формате") == 20 and str(div_film.find('div', {'class': 'clearfix'})) == "None":
                    print("Название фильма неизвестно: {} ".
                          format(session_list))
                else:
                    print("Название фильма: {} - {}".
                          format(div_film.find('div', {'class': 'clearfix'}).find('a').contents[0],
                                 session_list))

                    # if str(div_film.find('div', {'class': 'clearfix'})) == "None":
                    #     print("==================================================================== start")
                    #     print(div_film)
                    # print("---- {}".format(str(div_film.find('div', {'class': 'clearfix'}))))
                    # print(str(div_film.find('span', {'class': 'title'})).find("Сеансы в формате"))
                    # print("====================================================================   end")
                # разбираем верстку, удаляя лишний html и спец_символы

        except AttributeError:
            print("exception AttributeError")
            # exit(0)
