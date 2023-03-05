from PIL import Image, ImageDraw
import re


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


def decode():
    crosshair_code = "CSGO-OBFqv-K46Ei-F3Tk6-LdOdL-3aQ3A"
    DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
    SHARECODE_PATTERN = re.search("^CSGO(-?[\\w]{5}){5}$", crosshair_code)
    print(SHARECODE_PATTERN)
    pass

def create_image() -> object:
    img = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))
    img.save('crosshair.png', 'PNG')
    return img


def main():
    create_image()
    decode()


if __name__ == '__main__':
    main()
