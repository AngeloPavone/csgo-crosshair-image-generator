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


    def decode(SHARE_CODE: str) -> list:
        crosshair_code = SHARE_CODE[4:].replace('-','')

        DICTIONARY = "ABCDEFGHJKLMNOPQRSTUVWXYZabcdefhijkmnopqrstuvwxyz23456789"
        MATCH = re.search("^CSGO(-?[\\w]{5}){5}$", SHARE_CODE)

        if not MATCH:
            print('Not a Valid Crosshair Code!')
            exit(1)


        big = 0
        for char in list(crosshair_code[::-1]):
            big = (big * len(DICTIONARY)) + DICTIONARY.index(char)

        big_bytes = list(big.to_bytes(18)[::-1])

        if len(big_bytes) == 18:
            big_bytes.append(0x00)

        print(f'RAW BYTES: {big_bytes}')
        return big_bytes


    # TODO: add all the math and fix the ones that don't work
    def __init__(self, raw_bytes=decode(SHARE_CODE)) -> object:
        self.gap               =    (raw_bytes[3] / 10.0),
        self.outline           =    (raw_bytes[4] / 2.0),
        self.red               =    (raw_bytes[5]),
        self.green             =    (raw_bytes[6]),
        self.blue              =    (raw_bytes[7]),
        self.alpha             =    (raw_bytes[8]),
        self.split_distance    =    (raw_bytes[9]),
        self.hasOutline        =    (bytes[11] & 8) != 0,
        self.thickness         =    (raw_bytes[13] / 10.0),
        self.crosshair_style   =    (raw_bytes[14] & 0xF) >> 1,
        self.has_center_dot    =    ((raw_bytes[14] >> 4) & 1) != 0,
        self.has_alpha         =    ((bytes[14] >> 4) & 4) != 0,
        self.length            =    (raw_bytes[15] / 10.0),
        self.inner_split_alpha =    (bytes[11] >> 4) / 10.0,
        self.outer_split_alpha =    (bytes[12] & 0xF) / 10.0,
        self.split_size_ratio  =    (bytes[12] >> 4) / 10.0,
        self.is_t_style        =    ((bytes[14] >> 4) & 8) != 0,


def create_image() -> object:
    img = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))
    img.save('crosshair.png', 'PNG')
    return img


def main():
    create_image()
    c = Crosshair()

    print(f"")


if __name__ == '__main__':
    main()
