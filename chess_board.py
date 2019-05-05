from copy import deepcopy
from tkinter import *
from PIL import Image, ImageTk


WHITE = 'w'
BLACK = 'b'


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    '''Функция проверяет, что координаты (row, col) лежат
    внутри доски'''
    return 0 <= row < 8 and 0 <= col < 8


class Piece:
    def __init__(self, color):
        self.color = color

    def __eq__(self, other):
        return type(self) == type(other) and self.get_color() == other.get_color()

    def get_color(self):
        '''возращат цвет фигуры'''
        return self.color

    def can_move(self, board, row, col, row1, col1):
        '''can_move(self, board, row, col, row1, col1) -> возращает
        True в случае, если фигура может ходить на поле (row1, col1), иначе False.'''
        # если кооринаты не корректны, попытка пойти в тоже метсто, или в том месте, куда хочет пойти фигура,
        # есть своя фигура
        if row == row1 and col == col1 or not correct_coords(row, col) or not correct_coords(row1, col1) or\
           board.get_color_of_piece(row1, col1) == self.get_color():
            return False
        board1 = deepcopy(board)
        piece, board1.field[row][col] = board1.field[row][col], None
        board1.field[row1][col1] = piece

        king = King(self.get_color())
        for i in range(8):
            for j in range(8):
                if board1.get_piece(i, j) == king:
                    # свой король не подставляется под шах
                    return not board1.is_under_attack(i, j, opponent(self.get_color()))


class Knight(Piece):

    def char(self):
        '''возращает однобуквенное представление фигуры,
        в данном случае возращает "N".'''
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        return abs((row - row1) * (col - col1)) == 2 and\
            super().can_move(board, row, col, row1, col1)


class Bishop(Piece):

    def char(self):
        '''возращает однобуквенное представление фигуры,
        в данном случае возращает "B".'''
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 or col == col1:
            return False
        if abs(col - col1) == abs(row - row1):
            dir_col = abs(col1 - col) // (col1 - col)
            dir_row = abs(row1 - row) // (row1 - row)
            # в какую сторону шёл слон
            for i in range(1, abs(col1 - col)):
                if board.get_piece(row + i * dir_row, col + i * dir_col) is not None:
                    return False
            return super().can_move(board, row, col, row1, col1)
        else:
            return False


class Rook(Piece):

    def __init__(self, color, not_move=True):
        super().__init__(color)
        # для реализации рокировки
        self.not_move = not_move

    def char(self):
        '''возращает однобуквенное представление фигуры,
        в данном случае возращает "R".'''
        return 'R'

    def can_move(self, board, row, col, row1, col1):  # 3 2 6 5
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row == row1 and col == col1:
            return False
        if col == col1:
            in_cicle = abs(row - row1)  # будем проверять либо по вертикали, либо по горизонтали
            dir_row = abs(row1 - row) // (row1 - row)  # шёл вверх или вниз
            dir_col = 0

        elif row == row1:
            in_cicle = abs(col - col1)
            dir_row = 0
            dir_col = abs(col1 - col) // (col1 - col)  # шёл влево или вправо
        else:
            return False

        for i in range(1, in_cicle):
            if board.get_piece(row + i * dir_row, col + i * dir_col) is not None:
                # есть фигура на пути
                return False
        return super().can_move(board, row, col, row1, col1)


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        # не знаю, нужна ли это конструкция здесь
        # или нет, на всякий случай оставлю
        self.freshly_two_move = False
        # для реализации взятия на проходе

    def char(self):
        '''возращает однобуквенное представление фигуры,
        в данном случае возращает "P".'''
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.get_color() == WHITE:
            direction = 1
            start_row = 1
            take_on_pass = 4
        else:
            direction = -1
            start_row = 6
            take_on_pass = 3

        # ход на 1 клетку
        if row + direction == row1 and col == col1 and board.get_piece(row1, col1) is None:
            return super().can_move(board, row, col, row1, col1)

        # ход на 2 клетки из начального положения
        elif row == start_row and row + direction * 2 == row1 and col == col1 and\
                board.get_piece(row1, col1) is None:
            return super().can_move(board, row, col, row1, col1)

        # поедание по диагонали
        elif abs(col - col1) == 1 and row + direction == row1:
            # взятие на проходе
            if row == take_on_pass and\
               board.get_piece(row1 - direction, col1) == Pawn(opponent(self.get_color())) and\
               board.get_piece(row1 - direction, col1).freshly_two_move:
                return super().can_move(board, row, col, row1, col1)

            # обычное поедание
            return board.get_color_of_piece(row1, col1) == opponent(self.get_color()) and \
                super().can_move(board, row, col, row1, col1)

        else:
            return False


class Queen(Bishop, Rook):

    def char(self):
        '''возращает однобуквенное представление фигуры,
        в данном случае возращает "Q".'''
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        return Bishop(self.get_color()).can_move(board, row, col, row1, col1) or\
               Rook(self.get_color(), not_move=False).can_move(board, row, col, row1, col1)


class King(Piece):

    def __init__(self, color, not_move=True):
        super().__init__(color)
        # для реализации рокировки
        self.not_move = not_move

    def char(self):
        '''возращает однобуквенное представление фигуры,
        в данном случае возращает "K"'''
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if abs(col - col1) in {0, 1} and abs(row - row1) in {0, 1} and \
           ((row != row1 or col != col1) and correct_coords(row, col) and correct_coords(row1, col1) and
                board.get_color_of_piece(row1, col1) != self.get_color()):

            board1 = deepcopy(board)
            piece, board1.field[row][col] = board1.field[row][col], None
            board1.field[row1][col1] = piece
            return not board1.is_under_attack(row1, col1, opponent(self.get_color()))
        else:
            return False


class Board:
    def __init__(self):
        self.color = WHITE
        self.field = [[None] * 8 for _ in range(8)]
        self.winner = None

    def get_piece(self, row, col):
        '''Возращает фигуру, стоящую на клетке (row, col).'''
        return self.field[row][col]

    def get_color_of_piece(self, row, col):
        if self.get_piece(row, col) is not None:
            return self.get_piece(row, col).get_color()

    def cell(self, row, col):
        '''Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела.'''
        piece = self.field[row][col]
        if piece is None:
            return '  '
        # константы WHITE и BLACK содержат в себе один символ, который обозначает цвет
        return piece.get_color() + piece.char()

    def is_under_attack(self, row, col, color):  # 6 5 'w'
        '''Возращает True, если поле с координатами (row, col)
         находится под боем хотя бы одной фигуры цвета color.'''
        for i in range(len(self.field)):
            for j, piece in enumerate(self.field[i]):
                if piece is not None and piece.get_color() == color and\
                   piece.can_move(self, i, j, row, col):
                    return True

    def move_and_promote_pawn(self, row, col, row1, col1, char):
        if row == 6 and row1 == 7 and self.get_piece(row, col) == Pawn(WHITE) or \
                row == 1 and row1 == 0 and self.get_piece(row, col) == Pawn(BLACK):
            pieces = {'Q': Queen(self.color), 'R': Rook(self.color, not_move=False),
                      'B': Bishop(self.color), 'N': Knight(self.color)}
            pawn = self.get_piece(row, col)
            if pawn.can_move(self, row, col, row1, col1):
                if char in pieces:
                    self.field[row1][col1] = pieces[char]
                else:
                    return False
                self.field[row][col] = None
                self.color = opponent(self.color)
                return True
        return False

    def castling0(self):
        if self.color == WHITE:
            row = 0
        elif self.color == BLACK:
            row = 7

        if self.get_piece(row, 4) == King(self.color) and self.get_piece(row, 4).not_move and\
           self.get_piece(row, 0) == Rook(self.color) and self.get_piece(row, 0).not_move:

            # проверяем клетки между лодьёй и королём
            if self.is_under_attack(row, 4, opponent(self.color)):
                return False
            if self.get_piece(row, 1) is not None:
                return False
            for i in range(2, 4):
                if self.get_piece(row, i) is not None or\
                   self.is_under_attack(row, i, opponent(self.color)):
                    return False

            self.field[row][2], self.field[row][4] = self.field[row][4], self.field[row][2]
            self.field[row][0], self.field[row][3] = self.field[row][3], self.field[row][0]
            self.get_piece(row, 2).not_move = False
            self.get_piece(row, 3).not_move = False
            self.color = opponent(self.color)
            return True
        return False

    def castling7(self):
        if self.color == WHITE:
            row = 0
        else:
            row = 7

        if self.get_piece(row, 4) == King(self.color) and self.get_piece(row, 4).not_move and\
           self.get_piece(row, 7) == Rook(self.color) and self.get_piece(row, 7).not_move:

            # проверяем клетки между лодьёй и королём
            if self.is_under_attack(row, 4, opponent(self.color)):
                return False
            for i in range(5, 7):
                if self.get_piece(row, i) is not None or\
                   self.is_under_attack(row, i, opponent(self.color)):
                    return False

            self.field[row][6], self.field[row][4] = self.field[row][4], self.field[row][6]
            self.field[row][7], self.field[row][5] = self.field[row][5], self.field[row][7]
            self.get_piece(row, 6).not_move = False
            self.get_piece(row, 5).not_move = False
            self.color = opponent(self.color)
            return True
        return False

    def move_piece(self, row, col, row1, col1):
        '''Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт 'Ход успешен'.
        Если нет --- вернёт соотвествующую ошибку'''
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return 'Координаты не корректны'
        if row == row1 and col == col1:
            return 'Нельзя пойти в ту же клетку'

        piece = self.field[row][col]
        if piece is None:
            return 'Нужно ходить фигурой'
        if piece.get_color() != self.color:
            return 'Нельзя ходить фигурой противника'
        if not piece.can_move(self, row, col, row1, col1):
            return 'Фигура не может ходить в это место'

        if type(piece) in {King, Rook}:
            piece.not_move = False

        if type(piece) == Pawn:
            # взятие а проходе
            if self.get_piece(row1, col1) is None:
                if self.color == WHITE:
                    self.field[row1 - 1][col1] = None
                elif self.color == BLACK:
                    self.field[row1 + 1][col1] = None

        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        if type(piece) in {King, Rook}:
            piece.not_move = False
        elif type(piece) == Pawn:
            piece.freshly_two_move = abs(row - row1) == 2
        self.color = opponent(self.color)
        return 'Ход успешен'

    def check_mate(self):
        king, row, col, color = None, 0, 0, self.color
        # поиск короля и его координаты
        for i in range(8):
            for j in range(8):
                if type(self.get_piece(i, j)) == King and\
                   self.get_color_of_piece(i, j) == self.color:
                    king, row, col = self.get_piece(i, j), i, j

        # поиск угрожающих фигур
        list_of_threatening_pieces = []
        for i in range(8):
            for j, piece in enumerate(self.field[i]):
                if piece is not None and piece.get_color() == opponent(color) and\
                   piece.can_move(self, i, j, row, col):
                    list_of_threatening_pieces.append((piece, i, j))

        if len(list_of_threatening_pieces) == 0:
            # нет угрожающих фигур
            return True
        else:
            # куда может ходить король
            for i, j in [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                         (row, col - 1), (row, col + 1),
                         (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]:
                if king.can_move(self, row, col, i, j):
                    return True

            # если король никуда не может убежать, то ищем, как его закрыть от удара
            if len(list_of_threatening_pieces) == 1:
                threatening_piece, row_coor, col_coor = list_of_threatening_pieces[0]
                # угрожающая фигура, строка и колона, в которых она сидит
                if type(threatening_piece) in {Knight, Pawn}:
                    for i in range(8):
                        for j, piece in enumerate(self.field[i]):
                            # ищем фигуру, которая может съесть угрожающую фигуру
                            if piece is not None and piece.get_color() == color and \
                               piece.can_move(self, i, j, row_coor, col_coor):
                                return True
                    self.winner = opponent(col)
                    return False
                else:
                    dir_row = 0
                    dir_col = 0
                    # ищем фигуру, которая может встать между королём и угрожающей фигурой
                    if abs(row - row_coor) == abs(col - col_coor):
                        # если по диагонали
                        dir_col = abs(col_coor - col) // (col_coor - col)
                        dir_row = abs(row_coor - row) // (row_coor - row)
                    elif row == row_coor:
                        # если по горизонтали
                        dir_col = abs(col_coor - col) // (col_coor - col)
                        dir_row = 0
                    elif col == col_coor:
                        dir_col = 0
                        dir_row = abs(col_coor - col) // (col_coor - col)

                    for bet in range(1, abs(col_coor - col)):
                        for i in range(len(self.field)):
                            for j, piece in enumerate(self.field[i]):
                                board1 = deepcopy(self)
                                if board1.move_piece(i, j, row + i * dir_row, col + i * dir_col):
                                    return True
                    self.winner = opponent(col)
                    return False
            # если угрожающих фигур больше 1, то невозможно укрыться от них
            else:
                self.winner = opponent(col)
                return False


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main():
    # Создаём шахматную доску
    board = Board()

    board.field[0] = [
        Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
        King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
    ]
    board.field[1] = [
        Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
        Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
    ]
    board.field[6] = [
        Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
        Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
    ]
    board.field[7] = [
        Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
        King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
    ]

    # Цикл ввода команд игроков
    while True:
        # Выводим положение фигур на доске
        print_board(board)
        # Подсказка по командам
        print('Команды:')
        print('    exit                               -- выход')
        print('    move <row> <col> <row1> <col1>     -- ход из клетки (row, col)')
        print('                                          в клетку (row1, col1)')
        # Выводим приглашение игроку нужного цвета
        if not board.check_mate():
            if board.winner == WHITE:
                print('Победили Белые')
            elif board.winner == BLACK:
                print('Победили Чёрные')
            break
        if board.color == WHITE:
            print('Ход белых:')
        elif board.color == BLACK:
            print('Ход чёрных:')
        command = input()
        if command == 'exit':
            break
        move_type, row, col, row1, col1 = command.split()
        row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
        # выводит ошибку или успех
        print(board.move_piece(row, col, row1, col1))


def draw_chess_board(board):
    # experemental
    from PIL import Image, ImageDraw, ImageFont
    from string import ascii_uppercase
    dark = '#3F3F3F'
    fair = '#BDBDBD'
    mid = '#7F7F7F'
    image = Image.new('RGB', (1500, 1600), fair)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('C:/Windows/Fonts/Arial.ttf', 100)

    # внешняя ракма доски
    draw.rectangle([0, 0, 1499, 24], fill=mid)
    draw.rectangle([0, 1499, 1499, 1474], fill=mid)
    draw.rectangle([1499, 0, 1474, 1499], fill=mid)
    draw.rectangle([0, 0, 24, 1499], fill=mid)

    # внутренняя рамка доски
    draw.rectangle([125, 125, 1374, 149], fill=mid)
    draw.rectangle([125, 125, 149, 1374], fill=mid)
    draw.rectangle([1374, 125, 1349, 1374], fill=mid)
    draw.rectangle([125, 1374, 1374, 1349], fill=mid)

    box = lambda a: None
    list_of_letters = []
    if board.color == WHITE:
        for num in range(8, 0, -1):
            draw.text((90 - font.getsize(str(num))[1] // 2, (9 - num) * 150 + 15),
                      str(num), fill=mid, font=font)
            draw.text((1445 - font.getsize(str(num))[1] // 2, (9 - num) * 150 + 15),
                      str(num), fill=mid, font=font)
        list_of_letters = ascii_uppercase[:8]
        box = lambda row, col: ((col + 1) * 150 + 25, (8 - row) * 150 + 25)

    elif board.color == BLACK:
        for num in range(1, 9):
            draw.text((90 - font.getsize(str(num))[1] // 2, num * 150 + 15),
                      str(num), fill=mid, font=font)
            draw.text((1445 - font.getsize(str(num))[1] // 2, num * 150 + 15),
                      str(num), fill=mid, font=font)
        list_of_letters = reversed(ascii_uppercase[:8])
        box = lambda row, col: ((8 - col) * 150 + 25, (row + 1) * 150 + 25)

    for i, let in enumerate(list_of_letters):
        draw.text(((i + 1) * 150 + 75 - font.getsize(let)[0] // 2, 25),
                  let, fill=mid, font=font)
        draw.text(((i + 1) * 150 + 75 - font.getsize(let)[0] // 2, 1375),
                  let, fill=mid, font=font)

    for i in range(8):
        for j in range(8):
            if i % 2 + j % 2 == 1:
                draw.rectangle([(j + 1) * 150, (i + 1) * 150,
                                (j + 2) * 150 - 1, (i + 2) * 150 - 1], fill=dark)

    pieces = {'wP': 'white_pawn', 'wR': 'white_rook', 'wN': 'white_knight',
              'wB': 'white_bishop', 'wK': 'white_king', 'wQ': 'white_queen',
              'bP': 'black_pawn', 'bR': 'black_rook', 'bN': 'black_knight',
              'bB': 'black_bishop', 'bK': 'black_king', 'bQ': 'black_queen'}
    for row in range(8):
        for col in range(8):
            if board.cell(row, col) in pieces:
                name = 'images/' + pieces[board.cell(row, col)] + '.png'
                pil_im = Image.open(name)
                image.paste(pil_im, box=box(row, col), mask=pil_im)

    if board.winner is None:
        text = ''
        if board.color == WHITE:
            text = 'Ход Белых'
        elif board.color == BLACK:
            text = 'Ход Чёрных'
        draw.text((500, 1500), text, fill=dark, font=font)
    else:
        text = ''
        if board.winner == WHITE:
            text = 'Победили Белые'
        elif board.winner == BLACK:
            text = 'Победили Чёрные'
        draw.text((350, 1500), text, fill=dark, font=font)
    image.save('res.png',)


def GUI():
    root = Tk()
    canvas = Canvas(root, width=750, height=800)
    image = ImageTk.PhotoImage(Image.open("res.png").resize((750, 800)))
    imagesprite = canvas.create_image(375, 400, image=image)
    canvas.pack()
    root.mainloop()

