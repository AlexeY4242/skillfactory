# Наследуются другие классы
class BoardException(Exception):
    pass

# Выстрел за границы
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы пытаетесь выстрелить за пределы доски!"

# Стреляли в эту клетку
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

# Неправильное размещение корабля
class ShipPlacementException(BoardException):
    pass

# Описание точки с координатами
class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Точку атаковали или нет
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

# Строковое представление точки
    def __repr__(self):
        return f"Dot({self.x}, {self.y})"

# Корабль на поле
class Ship:
    def __init__(self, length, bow, orientation):
        self.length = length
        self.bow = bow  # Точка, где размещён нос корабля
        self.orientation = orientation  # Горизонтальная ('H') или вертикальная ('V')
        self.lives = length  # Количество жизней (точек корабля)

 #  Возвращает список всех точек корабля на основе его длины
    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            x = self.bow.x + i if self.orientation == 'H' else self.bow.x
            y = self.bow.y + i if self.orientation == 'V' else self.bow.y
            ship_dots.append(Dot(x, y))
        return ship_dots

# Инциализация доски
class Board:
    def __init__(self, hid=False):
        self.size = 6
        self.grid = [["O"] * self.size for _ in range(self.size)]
        self.ships = []
        self.hid = hid
        self.busy = []
        self.count = 0  # Количество уничтоженных кораблей

#  Добавляет корабль на доску
    def add_ship(self, ship):
        for dot in ship.dots:
            if self.out(dot) or dot in self.busy:
                raise ShipPlacementException()
        for dot in ship.dots:
            self.grid[dot.y][dot.x] = "■"
            self.busy.append(dot)

        self.ships.append(ship)
        self.contour(ship)

#  Обводит зону вокруг корабля
    def contour(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for dot in ship.dots:
            for dx, dy in near:
                cur = Dot(dot.x + dx, dot.y + dy)
                if not self.out(cur) and cur not in self.busy:
                    if verb:
                        self.grid[cur.y][cur.x] = "."
                    self.busy.append(cur)

    def out(self, dot):
        return not (0 <= dot.x < self.size and 0 <= dot.y < self.size)

    def shot(self, dot):
        if self.out(dot):
            raise BoardOutException()
        if dot in self.busy:
            raise BoardUsedException()

        self.busy.append(dot)

        for ship in self.ships:
            if dot in ship.dots:
                ship.lives -= 1
                self.grid[dot.y][dot.x] = "X"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)
                    print("Корабль уничтожен!")
                else:
                    print("Корабль ранен!")
                return True

        self.grid[dot.y][dot.x] = "T"
        print("Мимо!")
        return False

    def display(self):
        for row in self.grid:
            print(" ".join(row if not self.hid else ["O" if cell == "■" else cell for cell in row]))
        print()
class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)
class AI(Player):
    def ask(self):
        dot = Dot(random.randint(0, 5), random.randint(0, 5))

        print(f"Ход компьютера: {dot.x + 1} {dot.y + 1}")
        return dot

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()
            if len(cords) != 2:
                print("Введите 2 координаты!")
                continue

            x, y = cords
            if not (x.isdigit() and y.isdigit()):
                print("Введите числа!")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)
class Game:
    def __init__(self):
        self.user = None
        self.ai = None

    def random_board(self):
        board = None
        while board is None:
            try:
                board = Board()
                lens = [3, 2, 2, 1, 1, 1, 1]
                for l in lens:
                    while True:
                        try:
                            ship = Ship(l, Dot(random.randint(0, 5), random.randint(0, 5)), random.choice(['H', 'V']))
                            board.add_ship(ship)
                            break
                        except ShipPlacementException:
                            pass
                board.busy = []
            except Exception:
                pass
        return board

    def start(self):
        user_board = self.random_board()
        ai_board = self.random_board()
        ai_board.hid = True

        self.user = User(user_board, ai_board)
        self.ai = AI(ai_board, user_board)

        self.loop()

    def loop(self):
        while True:
            print("Ваша доска:")
            self.user.board.display()
            print("Доска компьютера:")
            self.ai.board.display()

            if self.user.move():
                continue
            if self.ai.move():
                continue

            if self.user.board.count == len(self.user.board.ships):
                print("Вы выиграли!")
                break
            if self.ai.board.count == len(self.ai.board.ships):
                print("Компьютер выиграл!")
                break
if __name__ == '__main__':
    game = Game()
    game.start()
