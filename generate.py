from PIL import Image, ImageDraw
import re
from math import log


SHARE_CODE = 'CSGO-2phoc-Nn9Pa-qrMFN-xtXZP-O3qRP'

SCALE = 1
WIDTH = 200
HEIGHT = 200
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2


class Crosshair:
    style               =   None
    has_center_dot      =   None
    size                =   None
    thickness           =   None
    gap                 =   None
    has_outline         =   None
    outline             =   None
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


    def decode(SHARE_CODE: str) -> list:

        def bytes_needed(n):
             if n == 0:
                  return 1
             return int(log(n, 256)) + 1

        crosshair_code = SHARE_CODE[4:].replace('-','')

        DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
        MATCH = re.search("^CSGO(-?[\\w]{5}){5}$", SHARE_CODE)

        if not MATCH:
            print('Not a Valid Crosshair Code!')
            exit(1)


        big = 0
        for char in list(crosshair_code[::-1]):
            big = (big * len(DICTIONARY)) + DICTIONARY.index(char)

        big_size = bytes_needed(big)
        big_bytes = list(big.to_bytes(big_size, 'big'))

        if len(big_bytes) == 18:
            big_bytes.insert(0x00, 0)

        # print(f'\n {big_bytes}\n')
        return big_bytes


    def __init__(self, raw_bytes=decode(SHARE_CODE)) -> None:
        self.style              =   (raw_bytes[14] & 0xF) >> 1
        self.is_t_style         =   (1 if ((raw_bytes[14] >> 4) & 8) != 0 else 0)
        self.size               =   (raw_bytes[15] / 10.0)
        self.thickness          =   (raw_bytes[13] / 10.0)
        self.gap                =   (float(raw_bytes[3] if raw_bytes[3] < 128 else raw_bytes[3] - 256) / 10.0)
        self.has_center_dot     =   (1 if ((raw_bytes[14] >> 4) & 1) != 0 else 0)
        self.has_alpha          =   (1 if ((raw_bytes[14] >> 4) & 4) != 0 else 0)
        self.alpha              =   (raw_bytes[8])
        self.outline            =   (raw_bytes[4] / 2.0)
        self.red                =   (raw_bytes[5])
        self.green              =   (raw_bytes[6])
        self.blue               =   (raw_bytes[7])
        self.has_outline        =   (1 if (raw_bytes[11] & 8) != 0 else 0)
        self.inner_split_alpha  =   (raw_bytes[11] >> 4) / 10.0
        self.outer_split_alpha  =   (raw_bytes[12] & 0xF) / 10.0
        self.split_distance     =   (raw_bytes[9])
        self.split_size_ratio   =   (raw_bytes[12] >> 4) / 10.0


def create_image() -> None:
    img = Image.new('RGBA', (WIDTH, HEIGHT), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    c = Crosshair()

    SIZE = (2 * c.size)
    THICKNESS = (c.thickness / 2)
    GAP = c.gap
    COLOR = "#87539f"

    SIZE = 44
    THICKNESS = 5
    GAP = 8

    # draw the rectangle on the image (left, top, right, bottom)
    # top
    if not c.is_t_style:
        draw.rectangle(((CENTER_X - THICKNESS) * SCALE, (CENTER_Y - GAP) * SCALE, (CENTER_X + THICKNESS) * SCALE, (CENTER_Y - SIZE) * SCALE), fill=COLOR, outline='black', width=1)
    # right
    draw.rectangle(((CENTER_X + GAP) * SCALE, (CENTER_Y + THICKNESS) * SCALE, (CENTER_X + SIZE) * SCALE, (CENTER_Y - THICKNESS) * SCALE), fill=COLOR, outline='black', width=1)
    # left
    draw.rectangle(((CENTER_X - SIZE) * SCALE, (CENTER_Y + THICKNESS) * SCALE, (CENTER_X - GAP) * SCALE, (CENTER_Y - THICKNESS) * SCALE), fill=COLOR, outline='black', width=1)
    # bottom
    draw.rectangle(((CENTER_X - THICKNESS) * SCALE, (CENTER_Y + SIZE) * SCALE, (CENTER_X + THICKNESS) * SCALE, (CENTER_Y + GAP) * SCALE), fill=COLOR, outline='black', width=1)


    img.save('crosshair.png', 'PNG')
    return img


def print_crosshair() -> None:
    c = Crosshair()
    print(f' CODE: {SHARE_CODE}\n')
    print(
            f' cl_crosshairstyle {c.style};\n'
            f' cl_crosshair_t {c.is_t_style};\n'
            f' cl_crosshairsize {c.size};\n'
            f' cl_crosshairthickness {c.thickness};\n'
            f' cl_crosshairgap {c.gap};\n'
            f' cl_crosshairdot {c.has_center_dot};\n\n'
            f' cl_crosshairusealpha {c.has_alpha};\n'
            f' cl_crosshairalpha {c.alpha};\n'
            f' cl_crosshair_drawoutline {c.has_outline};\n'
            f' cl_crosshaircolor 5;\n'
            f' cl_crosshaircolor_r {c.red};\n'
            f' cl_crosshaircolor_g {c.green};\n'
            f' cl_crosshaircolor_b {c.blue};\n\n'
            f' cl_crosshair_dynamic_splitdist {c.split_distance};\n'
            f' cl_crosshair_outlinethickness {c.outline};\n'
            f' cl_crosshair_dynamic_splitalpha_innermod {c.inner_split_alpha};\n'
            f' cl_crosshair_dynamic_splitalpha_outermod {c.outer_split_alpha};\n'
            f' cl_crosshair_dynamic_maxdist_splitratio {c.split_size_ratio}\n'
        )



def main():
    print_crosshair()
    create_image()


if __name__ == '__main__':
    main()
