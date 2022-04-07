per_cent = {'ТКБ': 5.6, 'СКБ': 5.9, 'ВТБ': 4.28, 'СБЕР': 4.0}
money = float(input("Введите сумму:\n"))
deposit = list(map(lambda summa: summa * money, list(per_cent.values())))
print(deposit)
print('Максимальная сумма, которую вы можете заработать - ', round(max(deposit), 2))
