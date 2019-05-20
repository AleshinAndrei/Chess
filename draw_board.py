# -*- coding: utf-8 -*-


def draw_chess_board():
    from PIL import Image, ImageDraw
    dark = '#3F3F3F'
    fair = '#BDBDBD'
    mid = '#7F7F7F'
    image = Image.new('RGBA', (750, 800), fair)
    draw = ImageDraw.Draw(image)

    # внешняя ракма доски
    draw.rectangle([0, 0, 749, 14], fill=mid)  # от левого верхнего до правого верхнего
    draw.rectangle([0, 0, 14, 749], fill=mid)  # от левого верхнего до левого нижнего
    draw.rectangle([749, 0, 735, 749], fill=mid)  # от правого верхнего до правого нижнего
    draw.rectangle([0, 749, 749, 735], fill=mid)  # от левого нижнего до правого нижнего

    # внутренняя рамка доски
    draw.rectangle([60, 60, 689, 74], fill=mid)  # от левого верхнего до правого верхнего
    draw.rectangle([60, 75, 74, 689], fill=mid)  # от левого верхнего до левого нижнего
    draw.rectangle([675, 75, 689, 689], fill=mid)  # от правого верхнего до правого нижнего
    draw.rectangle([75, 675, 689, 689], fill=mid)  # от левого нижнего до правого нижнего

    # Рисуем клетки
    for i in range(8):
        for j in range(8):
            if i % 2 + j % 2 == 1:
                draw.rectangle([(j + 1) * 75, (i + 1) * 75,
                                (j + 2) * 75 - 1, (i + 2) * 75 - 1], fill=dark)
    return image
