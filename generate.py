from PIL import Image, ImageDraw
import re


SHARE_CODE = "CSGO-zpstH-jozpK-AxiWq-GNC2a-pVnMC"


class Crosshair:
    style               =   None,
    has_center_dot      =   None,
    length              =   None,
    thickness           =   None,
    gap                 =   None,
    has_outline         =   None,
    outline             =   None,
    red                 =   None,
    green               =   None,
    blue                =   None,
    has_alpha           =   None,
    alpha               =   None,
    split_distance      =   None,
    inner_split_alpha   =   None,
    outer_split_alpha   =   None,
    split_size_ratio    =   None,
    is_t_style          =   None,


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
        self.gap                =   (raw_bytes[3] / 10.0)
        self.outline            =   (raw_bytes[4] / 2.0)
        self.red                =   (raw_bytes[5])
        self.green              =   (raw_bytes[6])
        self.blue               =   (raw_bytes[7])
        self.alpha              =   (raw_bytes[8])
        self.split_distance     =   (raw_bytes[9])
        self.has_outline        =   (1 if (raw_bytes[11] & 8) != 0 else 0)
        self.thickness          =   (raw_bytes[13] / 10.0)
        self.style              =   (raw_bytes[14] & 0xF) >> 1
        self.has_center_dot     =   (1 if ((raw_bytes[14] >> 4) & 1) != 0 else 0)
        self.has_alpha          =   (1 if ((raw_bytes[14] >> 4) & 4) != 0 else 0)
        self.length             =   (raw_bytes[15] / 10.0)
        self.inner_split_alpha  =   (raw_bytes[11] >> 4) / 10.0
        self.outer_split_alpha  =   (raw_bytes[12] & 0xF) / 10.0
        self.split_size_ratio   =   (raw_bytes[12] >> 4) / 10.0
        self.is_t_style         =   (1 if ((raw_bytes[14] >> 4) & 8) != 0 else 0)


def create_image() -> object:
    img = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))
    img.save('crosshair.png', 'PNG')
    return img


def main():
    create_image()
    c = Crosshair()
    print(f"cl_crosshairstyle {c.style}, cl_crosshair_t {c.is_t_style}, cl_crosshairsize {c.length}, cl_Crosshairthickness {c.thickness}, cl_crosshairgap {c.gap}, cl_crosshairdot {c.has_center_dot}, cl_crosshairusealpha {c.has_alpha}, cl_crosshairalpha {c.alpha}, cl_crosshair_drawoutline {c.has_outline}")



if __name__ == '__main__':
    main()
