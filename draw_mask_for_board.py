# -*- coding: utf-8 -*-


from chess_board import Board, WHITE


def draw_chess_mask(board):
    from PIL import ImageFont, Image, ImageDraw

    font = ImageFont.truetype('arial.ttf', 50)
    pieces = {'wP': 'white_pawn', 'wR': 'white_rook', 'wN': 'white_knight',
              'wB': 'white_bishop', 'wK': 'white_king', 'wQ': 'white_queen',
              'bP': 'black_pawn', 'bR': 'black_rook', 'bN': 'black_knight',
              'bB': 'black_bishop', 'bK': 'black_king', 'bQ': 'black_queen'}
    list_of_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    dark = '#3F3F3F'
    mid = '#7F7F7F'
    image = Image.new('RGBA', (750, 800), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    if board.color == WHITE:
        for num in range(8, 0, -1):
            # Рисуем цифры слева
            draw.text((45 - font.getsize(str(num))[1] // 2, (9 - num) * 75 + 7),
                      str(num), fill=mid, font=font)

            # Рисуем цифры справа
            draw.text((722 - font.getsize(str(num))[1] // 2, (9 - num) * 75 + 7),
                      str(num), fill=mid, font=font)

        def box(row, col):
            # для рисования фигур
            return (col + 1) * 75, (8 - row) * 75

    else:
        # для чёрного игрока цифры перевёрнуты
        for num in range(1, 9):
            # Рисуем цифры слева
            draw.text((45 - font.getsize(str(num))[1] // 2, num * 75 + 7),
                      str(num), fill=mid, font=font)
            # Рисуем цифры справа
            draw.text((722 - font.getsize(str(num))[1] // 2, num * 75 + 7),
                      str(num), fill=mid, font=font)
        # для чёрного игрока буквы развёрнуты на доске
        list_of_letters.reverse()

        def box(row, col):
            # для рисования фигур
            return (8 - col) * 75, (row + 1) * 75

    for i, let in enumerate(list_of_letters):
        draw.text(((i + 1) * 75 + 37 - font.getsize(let)[0] // 2, 12),
                  let, fill=mid, font=font)
        draw.text(((i + 1) * 75 + 37 - font.getsize(let)[0] // 2, 687),
                  let, fill=mid, font=font)

    for row in range(8):
        for col in range(8):
            if board.cell(row, col) in pieces:
                name = pieces[board.cell(row, col)] + '.png'
                piece_im = Image.open(name).resize((75, 75))
                image.paste(piece_im, box=box(row, col), mask=piece_im)

    if board.winner is None:
        if board.color == WHITE:
            text = 'Ход Белых'
        else:
            text = 'Ход Чёрных'
        draw.text((250, 750), text, fill=dark, font=font)
    else:
        if board.winner == WHITE:
            text = 'Победили Белые'
        else:
            text = 'Победили Чёрные'
        draw.text((175, 750), text, fill=dark, font=font)

    return image
