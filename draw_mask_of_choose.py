from PIL import Image
from chess_board import WHITE, BLACK


def draw_choose_mask(color):
    path = 'images/'
    name_queen = '_queen.png'
    name_rook = '_rook.png'
    name_bishop = '_bishop.png'
    name_knight = '_knight.png'
    if color == WHITE:
        name_color = 'white'
    elif color == BLACK:
        name_color = 'black'

    im_queen = Image.open(path + name_color + name_queen)
    im_rook = Image.open(path + name_color + name_rook)
    im_bishop = Image.open(path + name_color + name_bishop)
    im_knight = Image.open(path + name_color + name_knight)

    image = Image.new('RGBA', (750, 800), (192, 192, 192, 192))
    image.paste(im_queen, box=(150, 360), mask=im_queen)
    image.paste(im_rook, box=(275, 360), mask=im_rook)
    image.paste(im_bishop, box=(400, 360), mask=im_bishop)
    image.paste(im_knight, box=(525, 360), mask=im_knight)

    return image
