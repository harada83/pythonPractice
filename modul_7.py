import csv

# name.csv ниже нужно заменить на название csv файла, который вы хотите открыть
file_path = '/home/harada/skillbox/modul_7/click_stream.csv'
with open(file_path, mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date'])  # читаем файл

    #    home_page = 0
    #    search_page = 0
    #    payment_page = 0
    funnel = {}

    for row in csv_reader:  # перебираем по одной строчке нашего файла
        page = list(row.items())[1][1]  # так можно получить первый (не нулевой) элемент строки -
        # для нашего датасета это строка, указывающая, на какой страничке было совершено действие

        # ваш код для расчета воронки
        #       if page == '1_home_page':
        #           home_page += 1
        #       elif page == '2_search_page':
        #           search_page += 1
        #       elif page == '3_payment_page':
        #           payment_page += 1
        #       else:
        #           payment_confirmation_page += 1
        if page not in funnel:
            funnel[page] = 1
        else:
            funnel[page] += 1

print(funnel)
# print(
#    "home_page:", home_page,
#    "search_page:", search_page,
#    "payment_page:", payment_page,
#    "payment_confirmation_page:", payment_confirmation_page)
