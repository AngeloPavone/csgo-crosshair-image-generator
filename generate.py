from PIL import Image, ImageDraw
import re
from math import log


SHARE_CODE = 'CSGO-Cn37R-YE7vo-pLCAL-aURmZ-z6zkG'

SCALE = 1
WIDTH = 80
HEIGHT = 80
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2


class Crosshair:
    style               =   None
        # style 0 => Default
        # style 1 => Default static
        # style 2 => Classic
        # style 3 => Classic dynamic
        # style 4 => Classic static
    has_center_dot      =   None
    size                =   None
    thickness           =   None
    gap                 =   None
    fixed_gap           =   None
    has_outline         =   None
    outline_thickness   =   None
    red                 =   None
    green               =   None
    blue                =   None
    has_alpha           =   None
    alpha               =   None
    split_distance      =   None
    inner_split_alpha   =   None
    outer_split_alpha   =   None
    split_size_ratio    =   None
    is_t_style          =   None
    use_weapon_gap      =   None


    def code_to_bytes(SHARE_CODE: str) -> list:

        crosshair_code = SHARE_CODE[4:].replace('-','')

        DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
        MATCH = re.search("^CSGO(-?[\\w]{5}){5}$", SHARE_CODE)

        if not MATCH:
            print('Not a Valid Crosshair Code!')
            exit(1)

        big = 0
        for char in list(reversed(crosshair_code)):
            big = (big * len(DICTIONARY)) + DICTIONARY.index(char)

        def bytes_needed(n):
            return 1 if n == 0 else int(log(n, 256)) + 1

        bytes_required = bytes_needed(big)
        bytes = list(big.to_bytes(bytes_required, 'little'))

        if len(bytes) == 18:
            bytes.append(0x00)

        # print(f'\n {bytes}\n')
        return list(reversed(bytes))


    def uint8toint8(input: int) -> int:
        return input if input < 128 else input - 256

    def __init__(self,  bytes=code_to_bytes(SHARE_CODE)) -> None:
        self.gap                =   (Crosshair.uint8toint8(bytes[3]) / 10.0)
        self.outline_thickness  =   (bytes[4] / 2)
        self.red                =   (bytes[5])
        self.green              =   (bytes[6])
        self.blue               =   (bytes[7])
        self.alpha              =   (bytes[8])
        self.split_distance     =   (float(bytes[9]))
        self.fixed_gap          =   (Crosshair.uint8toint8((bytes[10]) / 10.0))
        self.color              =   (bytes[11] & 7)
        self.has_outline        =   (1 if (bytes[11] & 8) != 0 else 0)
        self.inner_split_alpha  =   (bytes[11] >> 4) / 10.0
        self.outer_split_alpha  =   (bytes[12] & 0xF) / 10.0
        self.split_size_ratio   =   (bytes[12] >> 4) / 10.0
        self.thickness          =   (bytes[13] / 10.0)
        self.has_center_dot     =   (1 if ((bytes[14] >> 4) & 1) != 0 else 0)
        self.use_weapon_gap     =   (1 if ((bytes[14] >> 4) & 2) != 0 else 0)
        self.has_alpha          =   (1 if ((bytes[14] >> 4) & 4) != 0 else 0)
        self.is_t_style         =   (1 if ((bytes[14] >> 4) & 8) != 0 else 0)
        self.style              =   (bytes[14] & 0xF) >> 1
        self.size               =   (bytes[15] / 10.0)


def create_image() -> None:
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    c = Crosshair()


    def map_gap_value(x: float) -> float:
        if x == -5:
            return 0
        if x > -5:
            return x -(-5)
        if x < -5:
            return (x + 5) * -1


    SIZE = (2 * c.size)
    THICKNESS = c.thickness
    GAP = map_gap_value(c.gap)
    OUTLINE = "BLACK" if c.has_outline else None

    # draw the rectangle on the image draw.rectangle(left, top, right, bottom)
    # top
    # draw.rectangle((top_left(THICKNESS, WIDTH), top_top(SIZE, HEIGHT), top_right(THICKNESS, WIDTH), top_bottom(SIZE, HEIGHT)), fill=(c.red, c.green, c.blue, c.alpha), outline=OUTLINE, width=1) if not c.is_t_style else None
    draw.rectangle(((CENTER_X - THICKNESS) * SCALE, (CENTER_Y - GAP) * SCALE, (CENTER_X + THICKNESS) * SCALE, (CENTER_Y - SIZE) * SCALE), fill=(c.red, c.green, c.blue, c.alpha), outline=OUTLINE, width=1) if not c.is_t_style else None
    # right
    draw.rectangle(((CENTER_X + GAP) * SCALE, (CENTER_Y + THICKNESS) * SCALE, (CENTER_X + SIZE) * SCALE, (CENTER_Y - THICKNESS) * SCALE), fill=(c.red, c.green, c.blue, c.alpha), outline=OUTLINE, width=1)
    # left
    draw.rectangle(((CENTER_X - SIZE) * SCALE, (CENTER_Y + THICKNESS) * SCALE, (CENTER_X - GAP) * SCALE, (CENTER_Y - THICKNESS) * SCALE), fill=(c.red, c.green, c.blue, c.alpha), outline=OUTLINE, width=1)
    # bottom
    draw.rectangle(((CENTER_X - THICKNESS) * SCALE, (CENTER_Y + SIZE) * SCALE, (CENTER_X + THICKNESS) * SCALE, (CENTER_Y + GAP) * SCALE), fill=(c.red, c.green, c.blue, c.alpha), outline=OUTLINE, width=1)


    img.save('crosshair.png', 'PNG')
    return img


def print_crosshair() -> None:
    c = Crosshair()
    print(f'\n CODE: {SHARE_CODE}\n')
    print(
            f' cl_crosshairgap {c.gap};\n'
            f' cl_crosshair_outlinethickness {c.outline_thickness};\n'
            f' cl_crosshaircolor_r {c.red};\n'
            f' cl_crosshaircolor_g {c.green};\n'
            f' cl_crosshaircolor_b {c.blue};\n'
            f' cl_crosshairalpha {c.alpha};\n\n'
            f' cl_crosshair_dynamic_splitdist {c.split_distance};\n'
            f' cl_fixedcrosshairgap {c.fixed_gap}\n'
            f' cl_crosshaircolor {c.color};\n'
            f' cl_crosshair_drawoutline {c.has_outline};\n'
            f' cl_crosshair_dynamic_splitalpha_innermod {c.inner_split_alpha};\n'
            f' cl_crosshair_dynamic_splitalpha_outermod {c.outer_split_alpha};\n\n'
            f' cl_crosshair_dynamic_maxdist_splitratio {c.split_size_ratio}\n'
            f' cl_crosshairthickness {c.thickness};\n'
            f' cl_crosshairdot {c.has_center_dot};\n'
            f' cl_crosshairgap_useweaponvalue {c.use_weapon_gap};\n'
            f' cl_crosshairusealpha {c.has_alpha};\n'
            f' cl_crosshair_t {c.is_t_style};\n'
            f' cl_crosshairstyle {c.style};\n'
            f' cl_crosshairsize {c.size};\n'
        )



def main():
    print_crosshair()
    create_image()


if __name__ == '__main__':
    main()
