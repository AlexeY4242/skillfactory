# Простая игра Крестики-нолики для начинающих

# Создаём пустое поле 3 на 3
pole = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]


# Функция для отображения поля
def pokazat_pole():
    for row in pole:
        print(row[0], row[1], row[2])


# Проверка победы
def proverit_pobedu(simvol):
    for i in range(3):
        # Проверяем строки
        if pole[i][0] == simvol and pole[i][1] == simvol and pole[i][2] == simvol:
            return True
        # Проверяем столбцы
        if pole[0][i] == simvol and pole[1][i] == simvol and pole[2][i] == simvol:
            return True
    # Проверяем диагонали
    if pole[0][0] == simvol and pole[1][1] == simvol and pole[2][2] == simvol:
        return True
    if pole[0][2] == simvol and pole[1][1] == simvol and pole[2][0] == simvol:
        return True
    return False


# Основная часть игры
hod = 0
while True:
    pokazat_pole()
    if hod % 2 == 0:
        print("Ходит X")
        simvol = 'X'
    else:
        print("Ходит O")
        simvol = 'O'

    # Запрос координат
    str = int(input("Введите номер строки (0-2): "))
    stolb = int(input("Введите номер столбца (0-2): "))

    if pole[str][stolb] == ' ':
        pole[str][stolb] = simvol
    else:
        print("Тут уже занято!")
        continue

    if proverit_pobedu(simvol):
        pokazat_pole()
        print("Победил", simvol)
        break

    hod += 1
    if hod == 9:
        pokazat_pole()
        print("Ничья!")
        break