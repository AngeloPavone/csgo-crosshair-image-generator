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
    print(len(big_bytes))

    # TODO: add a check to verify that its unsigned like this from the cshapr code
    '''
    // sometimes the number isn't unsigned, add a 00 byte at the end of the array to make sure it is
    if (all.Length == 18)
        all = all.Concat(new byte[] {0}).ToArray();
    return all.Reverse().ToArray();
    '''

    return big_bytes


# TODO: add all the math and fix the ones that don't work
def crosshair_info(raw_bytes=decode(SHARE_CODE)):
    Crosshair.outline = raw_bytes[4] / 2.0,
    Crosshair.red = raw_bytes[5],
    Crosshair.green = raw_bytes[6],
    Crosshair.blue = raw_bytes[7],
    Crosshair.alpha = raw_bytes[8],
    Crosshair.crosshair_style = ((raw_bytes[14] & 0xF) >> 1),
    Crosshair.has_center_dot = ((raw_bytes[14] >> 4) & 1) != 0,
    Crosshair.length = (raw_bytes[15] / 10.0),
    Crosshair.thickness = (raw_bytes[13] / 10.0),
    Crosshair.gap = (raw_bytes[3] / 10.0),
    Crosshair.hasOutline = None,
    Crosshair.split_distance = raw_bytes[9],
    Crosshair.has_alpha = None,
    Crosshair.inner_split_alpha = None,
    Crosshair.outer_split_alpha = None,
    Crosshair.split_size_ratio = None,
    Crosshair.is_t_style = None,


def create_image() -> object:
    img = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))
    img.save('crosshair.png', 'PNG')
    return img


def main():
    create_image()
    crosshair_info()


if __name__ == '__main__':
    main()
