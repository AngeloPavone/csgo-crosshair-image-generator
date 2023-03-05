from PIL import Image, ImageDraw


def generate_rectangle():
    img = Image.new('RGBA', (100, 100), (255, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle((25, 25, 75, 75), fill=(255, 0, 0))
    img.save('crosshair.png', 'PNG')
    print(f'crosshair generated')


def main():
    generate_rectangle()


if __name__ == '__main__':
    main()
