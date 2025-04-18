from byuimage import Image
import sys

IMAGE_FLAGS = ["-s", "-g", "-f", "-m"]


def check_flag(flag):
    if flag in IMAGE_FLAGS:
        return True
    else:
       return False
    
def apply_grayscale(image, output_file):
    for pixel in image:
        average = (pixel.blue + pixel.red + pixel.green) / 3
        pixel.red = average
        pixel.green = average
        pixel.blue = average
    image.save(output_file)

def apply_sepia(image, output_file):
    for pixel in image:
        true_red = 0.393*pixel.red + 0.769*pixel.green + 0.189*pixel.blue
        true_green = 0.349*pixel.red + 0.686*pixel.green + 0.168*pixel.blue
        true_blue = 0.272*pixel.red + 0.534*pixel.green + 0.131*pixel.blue
        pixel.red = true_red
        pixel.green = true_green
        pixel.blue = true_blue
        if pixel.red > 255:
            pixel.red = 255
        if pixel.green > 255:
            pixel.green = 255
        if pixel.blue > 255:
            pixel.blue = 255
    image.save(output_file)


def flip_vertically(image, output_file):
    flipped_image = Image.blank(image.width, image.height)
    for y in range(image.height):
        for x in range(image.width):
            flipped_image.get_pixel(x, y).red = image.get_pixel(x, image.height - y - 1).red
            flipped_image.get_pixel(x, y).green = image.get_pixel(x, image.height - y - 1).green
            flipped_image.get_pixel(x, y).blue = image.get_pixel(x, image.height - y - 1).blue
    flipped_image.save(output_file)


def flip_horizontally(image, output_file):
    flipped_image = Image.blank(image.width, image.height)
    for y in range(image.height):
        for x in range(image.width):
            flipped_image.get_pixel(x, y).red = image.get_pixel(image.width - x - 1, y).red
            flipped_image.get_pixel(x, y).green = image.get_pixel(image.width - x - 1, y).green
            flipped_image.get_pixel(x, y).blue = image.get_pixel(image.width - x - 1, y).blue
    flipped_image.save(output_file)

    
def process_image(given_flag):
    image = Image(sys.argv[2])
    if given_flag == "-g": # should have 2 arguments <input file> <output file>
        if len(sys.argv[2:]) > 2:
            raise ValueError("Too many arguments")
        elif len(sys.argv[2:]) < 2:
            raise ValueError("Not enough arguments")
        elif len(sys.argv[2:]) == 2:
            apply_grayscale(image, sys.argv[3])

    elif given_flag == "-s": # should have 2 arguments <input file> <output file>
        if len(sys.argv[2:]) > 2:
            raise ValueError("Too many arguments")
        elif len(sys.argv[2:]) < 2:
            raise ValueError("Not enough arguments")
        elif len(sys.argv[2:]) == 2:    
            apply_sepia(image, sys.argv[3])

    elif given_flag == "-f": # should have 2 arguments <input file> <output file>
        if len(sys.argv[2:]) > 2:
            raise ValueError("Too many arguments")
        elif len(sys.argv[2:]) < 2:
            raise ValueError("Not enough arguments")
        elif len(sys.argv[2:]) == 2:
            flip_vertically(image, sys.argv[3])

    elif given_flag == "-m": # should have 2 arguments <input file> <output file>
        if len(sys.argv[2:]) > 2:
            raise ValueError("Too many arguments")
        elif len(sys.argv[2:]) < 2:
            raise ValueError("Not enough arguments")
        elif len(sys.argv[2:]) == 2:
            flip_horizontally(image, sys.argv[3])

