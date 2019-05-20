# -*- coding: utf-8 -*-


from copy import deepcopy


WHITE = 'w'
BLACK = 'b'


def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def correct_coords(row, col):
    """Функция проверяет, что координаты (row, col) лежат
    внутри доски"""
    return 0 <= row < 8 and 0 <= col < 8


class Piece:
    def __init__(self, color):
        self.color = color

    def __eq__(self, other):
        return type(self) == type(other) and self.get_color() == other.get_color()

    def get_color(self):
        """возращат цвет фигуры"""
        return self.color

    def can_move(self, board, row, col, row1, col1):
        """can_move(self, board, row, col, row1, col1) -> возращает
        True в случае, если фигура может ходить на поле (row1, col1), иначе False."""
        # если кооринаты не корректны, попытка пойти в тоже метсто, или в том месте, куда хочет пойти фигура,
        # есть своя фигура
        if row == row1 and col == col1 or not correct_coords(row, col) or not correct_coords(row1, col1) or\
           board.get_color_of_piece(row1, col1) == self.get_color():
            return False
        board1 = deepcopy(board)
        piece, board1.field[row][col] = board1.field[row][col], None
        board1.field[row1][col1] = piece

        coord_of_king = board.find_king(self.get_color())
        if coord_of_king is not None:
            return not board1.is_under_attack(*coord_of_king, opponent(self.get_color()))
        else:
            return False


class Knight(Piece):
    def char(self):
        """возращает однобуквенное представление фигуры,
        в данном случае возращает "N"."""
        return 'N'

    def can_move(self, board, row, col, row1, col1):
        return correct_coords(row, col) and correct_coords(row1, col1) and\
               abs((row - row1) * (col - col1)) == 2 and\
               super().can_move(board, row, col, row1, col1)

    def can_move_at_all(self, board, row, col):
        for i, j in [(row + 2, col + 1), (row + 1, col + 2), (row - 1, col + 2), (row - 2, col + 1),
                     (row + 2, col - 1), (row + 1, col - 2), (row - 1, col - 2), (row - 2, col - 1)]:
            if self.can_move(board, row, col, i, j):
                return True
        return False


class Bishop(Piece):
    def char(self):
        """возращает однобуквенное представление фигуры,
        в данном случае возращает "B"."""
        return 'B'

    def can_move(self, board, row, col, row1, col1):
        if row == row1 or col == col1 or\
           not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if abs(col - col1) == abs(row - row1):
            dir_col = abs(col1 - col) // (col1 - col)
            dir_row = abs(row1 - row) // (row1 - row)
            # в какую сторону шёл слон
            for i in range(1, abs(col1 - col)):
                if board.get_piece(row + i * dir_row, col + i * dir_col) is not None:
                    return False
            return super().can_move(board, row, col, row1, col1)
        return False

    def can_move_at_all(self, board, row, col):
        for i, j in [(row + 1, col + 1), (row - 1, col + 1),
                     (row + 1, col - 1), (row - 1, col - 1)]:
            if self.can_move(board, row, col, i, j):
                return True
        return False


class Rook(Piece):
    def __init__(self, color, not_move=True):
        super().__init__(color)
        # для реализации рокировки
        self.not_move = not_move

    def char(self):
        """возращает однобуквенное представление фигуры,
        в данном случае возращает "R"."""
        return 'R'

    def can_move(self, board, row, col, row1, col1):  # 3 2 6 5
        # Невозможно сделать ход в клетку, которая не лежит в том же ряду
        # или столбце клеток.
        if row == row1 and col == col1 or \
           not correct_coords(row, col) or not correct_coords(row1, col1):
            return False

        if col == col1:
            in_cycle = abs(row - row1)  # будем проверять либо по вертикали, либо по горизонтали
            dir_row = abs(row1 - row) // (row1 - row)  # шёл вверх или вниз
            dir_col = 0
        elif row == row1:
            in_cycle = abs(col - col1)
            dir_row = 0
            dir_col = abs(col1 - col) // (col1 - col)  # шёл влево или вправо
        else:
            return False

        for i in range(1, in_cycle):
            if board.get_piece(row + i * dir_row, col + i * dir_col) is not None:
                # есть фигура на пути
                return False
        return super().can_move(board, row, col, row1, col1)

    def can_move_at_all(self, board, row, col):
        for i, j in [(row, col - 1), (row, col + 1),
                     (row - 1, col), (row + 1, col)]:
            if self.can_move(board, row, col, i, j):
                return True
        return False


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color)
        # не знаю, нужна ли это конструкция здесь
        # или нет, на всякий случай оставлю
        self.freshly_two_move = False
        # для реализации взятия на проходе

    def char(self):
        """возращает однобуквенное представление фигуры,
        в данном случае возращает "P"."""
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False

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
            return board.get_piece(row + direction, col) is None and\
                    super().can_move(board, row, col, row1, col1)

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

    def can_move_at_all(self, board, row, col):
        dir = 1 if self.get_color() == WHITE else -1
        for j in [col - 1, col, col + 1]:
            if self.can_move(board, row, col, row + dir, j):
                return True
        return False


class Queen(Bishop, Rook):
    def char(self):
        """возращает однобуквенное представление фигуры,
        в данном случае возращает "Q"."""
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
        return Bishop(self.get_color()).can_move(board, row, col, row1, col1) or\
               Rook(self.get_color(), not_move=False).can_move(board, row, col, row1, col1)

    def can_move_at_all(self, board, row, col):
        return Bishop(self.get_color()).can_move_at_all(board, row, col) or\
               Rook(self.get_color(), not_move=False).can_move_at_all(board, row, col)


class King(Piece):
    def __init__(self, color, not_move=True):
        super().__init__(color)
        # для реализации рокировки
        self.not_move = not_move

    def char(self):
        """возращает однобуквенное представление фигуры,
        в данном случае возращает "K"."""
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if correct_coords(row, col) and correct_coords(row1, col1) and\
           abs(col - col1) in {0, 1} and abs(row - row1) in {0, 1} and \
           ((row != row1 or col != col1) and
                board.get_color_of_piece(row1, col1) != self.get_color()):

            board1 = deepcopy(board)
            piece, board1.field[row][col] = board1.field[row][col], None
            board1.field[row1][col1] = piece
            return not board1.is_under_attack(row1, col1, opponent(self.get_color()))
        return False

    def can_move_at_all(self, board, row, col):
        for i in [row - 1, row, row + 1]:
            for j in [col - 1, col, col + 1]:
                if self.can_move(board, row, col, i, j):
                    return True
        return False


class Board:
    def __init__(self, *start_position):
        self.color = WHITE
        self.winner = None
        if not start_position:
            self.field = [
                [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
                 King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],

                [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
                 Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)]
            ] + [[None] * 8 for _ in range(4)] + [
                [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
                 Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],

                [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
                 King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]
            ]
        else:
            self.field = start_position[0]

    def get_piece(self, row, col):
        """Возращает фигуру, стоящую на клетке (row, col)."""
        return self.field[row][col]

    def get_color_of_piece(self, row, col):
        if self.get_piece(row, col) is not None:
            return self.get_piece(row, col).get_color()

    def cell(self, row, col):
        """Возвращает строку из двух символов. Если в клетке (row, col)
        находится фигура, символы цвета и фигуры. Если клетка пуста,
        то два пробела."""
        piece = self.field[row][col]
        if piece is None:
            return '  '
        # константы WHITE и BLACK содержат в себе один символ, который обозначает цвет
        return piece.get_color() + piece.char()

    def is_under_attack(self, row, col, color):
        """Возращает True, если поле с координатами (row, col)
         находится под боем хотя бы одной фигуры цвета color."""
        for i in range(len(self.field)):
            for j, piece in enumerate(self.field[i]):
                if piece is not None and piece.get_color() == color and\
                   piece.can_move(self, i, j, row, col):
                    return True
        else:
            return False

    def find_king(self, color):
        for i in range(8):
            for j in range(8):
                if self.get_piece(i, j) == King(color):
                    return i, j

    def move_and_promote_pawn(self, row, col, row1, col1, *char):
        pieces = {'Q': Queen(self.color), 'R': Rook(self.color, not_move=False),
                  'B': Bishop(self.color), 'N': Knight(self.color)}
        pawn = self.get_piece(row, col)
        if pawn.can_move(self, row, col, row1, col1):
            if char[0] in pieces:
                self.field[row1][col1] = pieces[char[0]]
            else:
                return False
            self.field[row][col] = None
            self.color = opponent(self.color)
            return True

    def castling0(self):
        """Если дальняя рокировка возможна, программаа вернёт True, если нет — вернёт False."""
        if self.color == WHITE:
            row = 0
        else:
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
            return True
        return False

    def castling7(self):
        """Если ближняя рокировка возможна, программаа вернёт True, если нет — вернёт False."""
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
            return True
        return False

    def move_piece(self, row, col, row1, col1, *char):
        """Переместить фигуру из точки (row, col) в точку (row1, col1).
        Если перемещение возможно, метод выполнит его и вернёт 'Ход успешен'.
        Если нет --- вернёт соотвествующую ошибку"""
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return 'Координаты не корректны'
        if row == row1 and col == col1:
            return 'Нельзя пойти в ту же клетку'

        piece = self.field[row][col]
        if piece is None:
            return 'Нужно ходить фигурой'
        if piece.get_color() != self.color:
            return 'Нельзя ходить фигурой противника'
        if row1 in {0, 7}:
            if col1 == 2 and self.castling0():
                self.field[row][2], self.field[row][4] = self.field[row][4], self.field[row][2]
                self.field[row][0], self.field[row][3] = self.field[row][3], self.field[row][0]
                self.get_piece(row, 2).not_move = False
                self.get_piece(row, 3).not_move = False
                self.color = opponent(self.color)
                return 'Дальняя рокировка успешна'
            elif col1 == 6 and self.castling7():
                self.field[row][6], self.field[row][4] = self.field[row][4], self.field[row][6]
                self.field[row][7], self.field[row][5] = self.field[row][5], self.field[row][7]
                self.get_piece(row, 6).not_move = False
                self.get_piece(row, 5).not_move = False
                self.color = opponent(self.color)
                return 'Ближняя рокировка успешна'
        if type(self.get_piece(row, col)) == Pawn and \
                (row == 6 and row1 == 7 and self.get_color_of_piece(row, col) == WHITE or
                 row == 1 and row1 == 0 and self.get_color_of_piece(row, col) == BLACK) and\
                self.move_and_promote_pawn(row, col, row1, col1, *char):
            return 'Ход успешен'
        if not piece.can_move(self, row, col, row1, col1):
            return 'Эта фигура не может ходить в это место'

        if type(piece) in {King, Rook}:
            piece.not_move = False
        elif type(piece) == Pawn:
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

    def checkmate(self):
        """Возращает True, если королю поставлен мат, иначе False."""
        color = self.color
        row, col = self.find_king(color)
        king = self.get_piece(row, col)

        if king.can_move_at_all(self, row, col):
            return False
        else:
            # поиск угрожающих фигур и своих фигур
            list_of_threatening_pieces = []
            list_of_my_pieces = []
            for i in range(8):
                for j, piece in enumerate(self.field[i]):
                    if piece is not None:
                        if piece.get_color() == color:
                            list_of_my_pieces.append((piece, i, j))
                        elif piece.get_color() == opponent(color) and \
                                piece.can_move(self, i, j, row, col):
                            list_of_threatening_pieces.append((piece, i, j))

            # если зажали в тиски
            if len(list_of_threatening_pieces) == 0:
                for piece, i, j in list_of_my_pieces:
                    if piece.can_move_at_all(self, i, j):
                        return False

            elif len(list_of_threatening_pieces) == 1:
                # ищем, как закрыть от удара короля
                threatening_piece, row_coor, col_coor = list_of_threatening_pieces[0]

                if type(threatening_piece) in {Knight, Pawn}:
                    # если угрожает конь или пешка, то их можно только съесть
                    for piece, i, j in list_of_my_pieces:
                        if piece.can_move(self, i, j, row_coor, col_coor):
                            return False
                else:
                    # если угрожает слон, лодья или ферзь
                    # то определяем, откуда угрожают
                    dir_row = 0
                    dir_col = 0
                    in_cycle = abs(col_coor - col) + 1
                    if abs(row - row_coor) == abs(col - col_coor):
                        # если по диагонали
                        dir_col = abs(col_coor - col) // (col_coor - col)
                        dir_row = abs(row_coor - row) // (row_coor - row)
                    elif row == row_coor:
                        # если по горизонтали
                        dir_col = abs(col_coor - col) // (col_coor - col)
                        dir_row = 0
                    elif col == col_coor:
                        # если по вертикали
                        dir_col = 0
                        dir_row = abs(row_coor - row) // (row_coor - row)
                        in_cycle = abs(row_coor - row) + 1
                    # ищем фигуру, которая может встать между королём и угрожающей фигурой
                    for bet in range(1, in_cycle):
                        for piece, i, j in list_of_my_pieces:
                            if piece.can_move(self, i, j, row + dir_row * bet, col + dir_col * bet):
                                return False

            # если угрожающих фигур больше 1
            # или нельзя ходить ничем никуда
            # или нельзя съесть угрожающую фигуру
            # или нелья встать между угрожающей фигурой и королём
            self.winner = opponent(col)
            return True


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(f'  {row}  ', end='')
        for col in range(8):
            print(f'| {board.cell(row, col)} ', end='')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()


def main(*start_position):
    # Создаём шахматную доску
    board = Board(*start_position)

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
        if board.checkmate():
            if board.winner == WHITE:
                print('Победили Белые')
            else:
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
        try:
            print(board.move_piece(row, col, row1, col1))
        except TypeError:
            print('Введите букву фигуры')
            char = input()
            print(board.move_piece(row, col, row1, col1, char))
