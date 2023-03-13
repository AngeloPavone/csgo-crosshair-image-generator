from os import walk
from PIL import Image, ImageDraw
import re
from math import log


SHARE_CODE = 'CSGO-D9YFQ-V9cWf-LecTD-j4PkT-pVnMC'

WIDTH = 961
HEIGHT = 541
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2


class Crosshair:
    style               =  0
    has_center_dot      =  0
    size                =  0.0
    thickness           =  0.0
    gap                 =  0.0
    fixed_gap           =  0
    has_outline         =  0
    outline_thickness   =  0.0
    red                 =  0
    green               =  0
    blue                =  0
    has_alpha           =  0
    alpha               =  0
    split_distance      =  0
    inner_split_alpha   =  0
    outer_split_alpha   =  0
    split_size_ratio    =  0
    is_t_style          =  0
    use_weapon_gap      =  0

    def code_to_bytes(self, SHARE_CODE: str) -> list:

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

        return list(reversed(bytes))


    def uint8toint8(self, input: int) -> int:
        return input if input < 128 else input - 256


    def __init__(self, raw_bytes=None) -> None:
        raw_bytes = self.code_to_bytes(SHARE_CODE)
        print(raw_bytes)
        self.gap                =   (self.uint8toint8(raw_bytes[3]) / 10.0)
        self.outline_thickness  =   (raw_bytes[4] / 2)
        self.red                =   (raw_bytes[5])
        self.green              =   (raw_bytes[6])
        self.blue               =   (raw_bytes[7])
        self.alpha              =   (raw_bytes[8])
        self.split_distance     =   (float(raw_bytes[9]))
        self.fixed_gap          =   (self.uint8toint8((raw_bytes[10]) / 10.0))
        self.color              =   (raw_bytes[11] & 7)
        self.has_outline        =   (1 if (raw_bytes[11] & 8) != 0 else 0)
        self.inner_split_alpha  =   (raw_bytes[11] >> 4) / 10.0
        self.outer_split_alpha  =   (raw_bytes[12] & 0xF) / 10.0
        self.split_size_ratio   =   (raw_bytes[12] >> 4) / 10.0
        self.thickness          =   (raw_bytes[13] / 10.0)
        self.has_center_dot     =   (1 if ((raw_bytes[14] >> 4) & 1) != 0 else 0)
        self.use_weapon_gap     =   (1 if ((raw_bytes[14] >> 4) & 2) != 0 else 0)
        self.has_alpha          =   (1 if ((raw_bytes[14] >> 4) & 4) != 0 else 0)
        self.is_t_style         =   (1 if ((raw_bytes[14] >> 4) & 8) != 0 else 0)
        self.style              =   (raw_bytes[14] & 0xF) >> 1
        self.size               =   (raw_bytes[15] / 10.0)


def create_image() -> object:
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    c = Crosshair()


    def map_gap_value(x: float) -> float:
        print(x)
        if x > -5:
            return x -(-5)
        elif x < -5:
            return (x + 5) * -1
        else:
            return 0

    SIZE = 4 * float(c.size)
    print(SIZE)
    THICKNESS = 4 * float(c.thickness)
    print(THICKNESS)
    GAP = 2 * float(map_gap_value(c.gap))
    print(GAP)
    OUTLINE = 1 if c.has_outline else 0


    print(f'resolution: ({WIDTH}, {HEIGHT})')
    def left() -> tuple:
        X1 = CENTER_X - (SIZE + (GAP / 2)) + 1
        Y1 = CENTER_Y + (THICKNESS / 2)
        X2 = CENTER_X - (GAP / 2)  + 1
        Y2 = CENTER_Y - (THICKNESS / 2)
        left = tuple([X1, Y1, X2, Y2])
        print(f'left: {left}')
        return left


    def top() -> tuple:
        X1 = CENTER_X - (THICKNESS / 2)
        Y1 = CENTER_Y - (SIZE + (GAP / 2)) + 1
        X2 = CENTER_X + (THICKNESS / 2)
        Y2 = CENTER_Y - (GAP / 2) + 1
        top = tuple([X1, Y1, X2, Y2])
        print(f'top: {top}')
        return top


    def right() -> tuple:
        X1 = CENTER_X + (GAP / 2) - 1
        Y1 = CENTER_Y + (THICKNESS / 2)
        X2 = CENTER_X + (SIZE + (GAP / 2)) - 1
        Y2 = CENTER_Y - (THICKNESS / 2)
        right = tuple([X1, Y1, X2, Y2])
        print(f'right: {right}')
        return right


    def bottom() -> tuple:
        X1 = CENTER_X - (THICKNESS / 2)
        Y1 = CENTER_Y + (GAP / 2) - 1
        X2 = CENTER_X + (THICKNESS / 2)
        Y2 = CENTER_Y + (SIZE + (GAP / 2)) - 1
        bottom = tuple([X1, Y1, X2, Y2])
        print(f'bottom: {bottom}')
        return bottom


    draw.rectangle((left()), fill=(c.red, c.green, c.blue, c.alpha), outline="black", width=OUTLINE)
    draw.rectangle((top()), fill=(c.red, c.green, c.blue, c.alpha), outline="black", width=OUTLINE)
    draw.rectangle((right()), fill=(c.red, c.green, c.blue, c.alpha), outline="black", width=OUTLINE)
    draw.rectangle((bottom()), fill=(c.red, c.green, c.blue, c.alpha), outline="black", width=OUTLINE)


    img.save('crosshair.png', 'PNG')
    return img


def print_crosshair() -> None:
    c = Crosshair()
    print(f'\n CODE: \n {SHARE_CODE}\n')

    print(f' OUTPUT: ')
    print(
            f' cl_crosshairstyle {c.style};\n'
            f' cl_crosshairsize {c.size};\n'
            f' cl_crosshairthickness {c.thickness};\n'
            f' cl_crosshairgap {c.gap};\n'
            f' cl_crosshair_drawoutline {c.has_outline};\n'
            f' cl_crosshair_outlinethickness {c.outline_thickness};\n'
            f' cl_crosshaircolor {c.color};\n'
            f' cl_crosshaircolor_r {c.red};\n'
            f' cl_crosshaircolor_g {c.green};\n'
            f' cl_crosshaircolor_b {c.blue};\n'
            f' cl_crosshairusealpha {c.has_alpha};\n'
            f' cl_crosshairalpha {c.alpha};\n'
            f' cl_crosshairdot {c.has_center_dot};\n'
            f' cl_crosshair_t {c.is_t_style};\n'
            f' cl_crosshairgap_useweaponvalue {c.use_weapon_gap};\n'
            f' cl_crosshair_dynamic_splitdist {c.split_distance};\n'
            f' cl_fixedcrosshairgap {c.fixed_gap};\n'
            f' cl_crosshair_dynamic_splitalpha_innermod {c.inner_split_alpha};\n'
            f' cl_crosshair_dynamic_splitalpha_outermod {c.outer_split_alpha};\n'
            f' cl_crosshair_dynamic_maxdist_splitratio {c.split_size_ratio};\n'
       )



def main():
    print_crosshair()
    create_image()


if __name__ == '__main__':
    main()
