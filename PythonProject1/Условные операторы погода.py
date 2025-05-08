#Запрашиваем ввод температуры
temperature = int(input("Input temperature: "))

#для указания начальных статусов дождливости воспользуемся False или None
rainy = None
heavyRain = None

#если температура <0 то про дождь спрашивать бессмысленно
if temperature > 0:
   rainy = input("Is rainy: ") == "yes"
#если идет дождь спросим насколько он серьезный
   if rainy:
       heavyRain = input("Is heavy rain: ") == "yes"


#реализуем логику по схеме
decision = "Не решил что брать. Останусь дома."
if (temperature) > 20 and (temperature < 30) :
   if rainy:
       decision = "Взять футболку шорты и дождевик"
   else:
       decision = "Взять футболку и шорты"
elif temperature > 0:
   if rainy:
       if heavyRain:
           decision = "Взять пальто, резиновые сапоги и зонт"
       else:
           decision = "Взять пальто и дождевик"
   else:
       decision = "Взять пальто"
else:
   decision = "Взять пуховик"


#Выведем наше решение на экран
print(decision)