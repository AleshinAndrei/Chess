from tkinter import *
from PIL import Image, ImageTk
from chess_board import Board, WHITE, BLACK, opponent
from draw_mask_for_board import draw_mask
from draw_mask_of_cells import draw_cells_mask
from draw_mask_of_choose import draw_choose_mask


def choose_click(event, board, row, col, row1, col1):
    x = event.x
    y = event.y
    if True:
        char = ''
        board.move_piece(row, col, row1, col1, char)
    else:
        root.bind('<Button-1>', lambda event: choose_click(event, board, row, col, row1, col1))


def click(event, status, board, image_of_board):
    x = event.x
    y = event.y
    list_of_can_move = []

    coor_of_king = board.find_king(board.color)
    list_of_threatening_pieces = []
    for i in range(8):
        for j, piece in enumerate(board.field[i]):
            if piece is not None and piece.get_color() == opponent(board.color) and \
                    piece.can_move(board, i, j, *coor_of_king):
                list_of_threatening_pieces.append((i, j))
    if list_of_threatening_pieces:
        status['dangerous'] = (coor_of_king, list_of_threatening_pieces)
    else:
        status['dangerous'] = None

    if 75 <= x <= 675 and 75 <= y <= 675:
        row = 0
        col = 0
        # принцип 'кто считает'
        if board.color == WHITE:
            row = 7 - (y - 75) // 75
            col = (x - 75) // 75
        elif board.color == BLACK:
            row = (y - 75) // 75
            col = 7 - (x - 75) // 75

        if status['active'] is None:
            piece = board.get_piece(row, col)
            if piece is not None:
                status['active'] = (row, col)
                for i in range(8):
                    for j in range(8):
                        if piece.can_move(board, row, col, i, j):
                            list_of_can_move.append((i, j))
        else:
            try:
                board.move_piece(*status['active'], row, col)
            except TypeError:
                # если потребуется фигура для замены пешки
                choose_mask = draw_choose_mask(board.color)
                cells_mask = draw_cells_mask(status, board.color)
                pieces_mask = draw_mask(board)
                image_of_board.paste(cells_mask, mask=cells_mask)
                image_of_board.paste(pieces_mask, mask=pieces_mask)
                image_of_board.paste(choose_mask, mask=choose_mask)
                canvas.create_image(375, 400, image=image_of_board)
                root.bind('<Button-1>', lambda event: choose_click(event, board, *status['active'], row, col))
            status['active'] = None
    else:
        status['active'] = None

    if board.checkmate():
        print(board.winner)
        root.destroy()
    cells_mask = draw_cells_mask(status, list_of_can_move, board.color)
    pieces_mask = draw_mask(board)
    image_of_board.paste(cells_mask)
    image_of_board.paste(pieces_mask)
    canvas.create_image(375, 400, image=image_of_board)
    canvas.pack()


class StartClick:
    def __init__(self):
        self.x = 0
        self.y = 0


root = Tk()
image = ImageTk.PhotoImage(Image.open('res.png'))
board = Board()
status = {'active': None, 'dangerous': None}
canvas = Canvas(root, width=750, height=800)
click(StartClick(), status, board, image)
root.bind('<Button-1>', lambda event: click(event, status, board, image))
root.mainloop()
