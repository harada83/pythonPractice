import csv

funnel_by_month = {}  # создаем словарь, где будут храниться словари за каждый месяц
funnel_template = {'1_home_page': 0, '2_search_page': 0, '3_payment_page': 0, '4_payment_confirmation_page': 0}

with open('/home/harada/skillbox/modul_7/click_stream2.csv', mode='r') as csv_file:  # открываем файл
    csv_reader = csv.DictReader(csv_file, fieldnames=['ID', 'page', 'date'])  # читаем файл

    # проходим циклом по объекту csv_reader
    for row in csv_reader:  # берем строку из объекта csv_reader

        page = list(row.items())[1][1]  # вытаскиваем название страницы
        event_date = list(row.items())[2][1][:-3]  # вытаскиваем дату в формате YYYY-MM

        # проверяем существует ли ключ со значением event_date в словаре
        if event_date not in funnel_by_month:  # если нет
            funnel_by_month[event_date] = funnel_template.copy()  # создаем ключ, в значение копируем заготовку

        # проверяем условиями и прибавляем единицу к нужному ключу в словаре
        if page == '1_home_page':
            funnel_by_month[event_date]['1_home_page'] += 1
        elif page == '2_search_page':
            funnel_by_month[event_date]['2_search_page'] += 1
        elif page == '3_payment_page':
            funnel_by_month[event_date]['3_payment_page'] += 1
        else:
            funnel_by_month[event_date]['4_payment_confirmation_page'] += 1

print(funnel_by_month)
