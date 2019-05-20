# -*- coding: utf-8 -*-
from chess_board import Board, WHITE, BLACK
from PIL import Image, ImageDraw


def draw_cells_mask(status, list_of_can_move, color):
    image = Image.new('RGBA', (750, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    box = lambda a: None
    if color == WHITE:
        box = lambda row, col: [(col + 1) * 75, (8 - row) * 75,
                                (col + 2) * 75 - 1, (9 - row) * 75 - 1]
    elif color == BLACK:
        box = lambda row, col: [(8 - col) * 75, (row + 1) * 75,
                                (9 - col) * 75 - 1, (row + 2) * 75 - 1]

    if status['dangerous'] is not None:
        for i, j in status['dangerous'][1]:
            draw.rectangle(box(i, j), fill=(139, 0, 0, 127))
        row, col = status['dangerous'][0]
        draw.rectangle(box(row, col), fill=(255, 0, 0, 127))

    for i, j in list_of_can_move:
        draw.rectangle(box(i, j), fill=(106, 90, 205, 127))
    return image
