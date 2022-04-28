kol = int(input('Введите количество участников: '))
sum = 0
for i in range(kol):
    vozr = int(input('Введите возраст ' + str(i+1) + ' участника: '))
    if vozr >= 25:
        print((i + 1), 'билет будет стоить 1390Р')
        sum += 1390
    elif 18 < vozr < 25:
        sum += 990
        print((i + 1), 'билет будет стоить 990Р')
    else:
        print((i + 1), 'билет будет бесплатным')
if kol > 3:
    print('Общая сумма с учетом скидки 10% равна:', sum*0.9)
else:
    print('Общая сумма равна:', sum)
