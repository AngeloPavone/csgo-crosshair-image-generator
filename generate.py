from PIL import Image, ImageDraw
import re


SHARE_CODE = "CSGO-zpstH-jozpK-AxiWq-GNC2a-pVnMC"


class Crosshair:
    crosshair_style = None,     # LODWORD [14] >> 1
    has_center_dot = None,      # HIDWORD [14] & 1
    length = None,              # [15] / 10
    thickness = None,           # [13] / 10
    gap = None,                 # unchecked((sbyte) [3]) / 10
    hasOutline = None,          # [11] & 8
    outline = None,             # [4] / 2
    red = None,                 # [5]
    green = None,               # [6]
    blue = None,                # [7]
    has_alpha = None,           # HIDWORD [14] & 4
    alpha = None,               # [8]
    split_distance = None,      # [9]
    inner_split_alpha = None,   # HIDWORD [11] / 10
    outer_split_alpha = None,   # LODWORD [12] / 10
    split_size_ratio = None,    # HIDWORD [12] / 10
    is_t_style = None,          # HIDWORD [14] & 8


def decode(SHARE_CODE):
    DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
    MATCH = re.search("^CSGO(-?[\\w]{5}){5}$", SHARE_CODE)
    if not MATCH:
        print('Not a Valid Crosshair Code!')
        exit(1)

    crosshair_code = SHARE_CODE[4:].replace('-','')

    big = 0
    for char in list(crosshair_code[::-1]):
        big = (big * len(DICTIONARY)) + DICTIONARY.index(char)

    big_bytes = list(big.to_bytes(18)[::-1])
    print(big_bytes)


    print(crosshair_code)

def create_image() -> object:
    img = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))
    img.save('crosshair.png', 'PNG')
    return img


def main():
    create_image()
    decode(SHARE_CODE)


if __name__ == '__main__':
    main()
