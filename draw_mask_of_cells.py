# -*- coding: utf-8 -*-


from chess_board import Board, WHITE, BLACK
from PIL import Image, ImageDraw


def draw_cells_mask(status, list_of_can_move, color):
    image = Image.new('RGBA', (750, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if color == WHITE:
        def box(row, col):
            return [(col + 1) * 75, (8 - row) * 75,
                    (col + 2) * 75 - 1, (9 - row) * 75 - 1]
    else:
        def box(row, col):
            return [(8 - col) * 75, (row + 1) * 75,
                    (9 - col) * 75 - 1, (row + 2) * 75 - 1]

    if status['dangerous'] is not None:
        for i, j in status['dangerous'][1]:
            draw.rectangle(box(i, j), fill=(139, 0, 0, 127))
        row, col = status['dangerous'][0]
        draw.rectangle(box(row, col), fill=(255, 0, 0, 127))

    for i, j in list_of_can_move:
        draw.rectangle(box(i, j), fill=(106, 90, 205, 127))

    if color == WHITE and status['active'] == (0, 4):
            if status['castling0']:
                draw.rectangle([225, 600, 299, 674], fill=(240, 230, 140, 127))
            if status['castling7']:
                draw.rectangle([525, 600, 599, 674], fill=(240, 230, 140, 127))

    elif color == BLACK and status['active'] == (7, 4):
        if status['castling0']:
            draw.rectangle([450, 600, 524, 674], fill=(240, 230, 140, 127))
        if status['castling7']:
            draw.rectangle([150, 600, 224, 674], fill=(240, 230, 140, 127))

    return image
