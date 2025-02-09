import pandas as pd
import csv

data = ['Тип продукта Йогурт питьевой', 'Бренд Домик в Деревне', 'Производитель Вимм-Билль-Данн',
        'Вес, кг 0.26', 'Тип упаковки пластиковая бутылка', 'Тип молока Коровье',
        'Вкусовая добавка Без вкусовой добавки',
        'Жирность, % 1.8', 'Консистенция Питьевой', 'Фермерский продукт Нет', 'Артикул 1000567712',
        'Мин. температура хранения, °C 2', 'Макс. температура хранения, °C 6', 'Срок годности, дней 40']

name_column = ['Название', 'Тип продукта', 'Бренд', 'price', 'date_price']


def transformation(description_list, name_column):
    data = []
    for i in name_column:
        for j in description_list[0].split(','):
            if i in j:
                data.append(j.replace(i, '').lstrip())
    return data


df = pd.DataFrame(columns=name_column)
with open('products_magnit.csv', 'r', encoding='utf-8') as f:
    x = 0
    for i in csv.reader(f):
        data_list = transformation(i, name_column)
        if data_list:
            df.loc[x] = transformation(i, name_column)[:-1]
            x += 1

df1 = pd.DataFrame(columns=name_column)
with open('products.csv', 'r', encoding='utf-8') as f:
    x = 0
    for i in csv.reader(f):
        print(i)
        data_list1 = transformation([','.join(i)], name_column)
        if data_list1:
            try:
                df1.loc[x] = transformation([','.join(i)], name_column)[:-1]
                x += 1
            except ValueError:
                pass

print(df.merge(df1, on=['Тип продукта', 'Бренд']))


