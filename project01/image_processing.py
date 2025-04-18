from byuimage import Image
import sys

given_flag = sys.argv[1]

# flags = [display image, grayscale, sepia, darken, borders, flip vertically, flip horizontally, create collage, greenscreen (r for remove backgroud)]
flags = ["-d", "-g", "-s", "-k", "-b","-f", "-m", "-c", "-y"]


def check_flag(flag):
    if flag in flags:
        return True
    else:
       return False
    
def display_image(image):
    image.show()

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

def apply_darken(image, output_file, percent):
    percent = float(percent)
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.get_pixel(x, y)
            pixel.red *= 1 - percent
            pixel.green *= 1 - percent
            pixel.blue *= 1 - percent
    image.save(output_file)

def apply_borders(image, output_file, thickness, red, green, blue):
    thickness = int(thickness)
    red = int(red)
    green = int(green)
    blue = int(blue)
    bordered_image = Image.blank(image.width + (2 * thickness), image.height + (2 * thickness))
    for y in range(bordered_image.height):
        for x in range(bordered_image.width):
            if y < thickness or y > bordered_image.height - thickness - 1 or x < thickness or x > bordered_image.width - thickness - 1:
                bordered_image.get_pixel(x, y).red = red
                bordered_image.get_pixel(x, y).green = green
                bordered_image.get_pixel(x, y).blue = blue
            elif y >= thickness and y <= bordered_image.height - thickness - 1 and x >= thickness and x <= bordered_image.width - thickness - 1:
                bordered_image.get_pixel(x, y).red = image.get_pixel(x - thickness, y - thickness).red
                bordered_image.get_pixel(x, y).green = image.get_pixel(x - thickness, y - thickness).green
                bordered_image.get_pixel(x, y).blue = image.get_pixel(x - thickness, y - thickness).blue
    bordered_image.save(output_file)

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

def create_collage(image1, image2, image3, image4, output_file, thickness):
    thickness = int(thickness)
    image1 = Image(image1)
    image2 = Image(image2)
    image3 = Image(image3)
    image4 = Image(image4)
    collage = Image.blank(image1.width + image2.width + thickness * 3, image1.height + image3.height + thickness * 3)
    for y in range(collage.height):
            for x in range(collage.width):
                # Top border
                if y < thickness:
                    collage.get_pixel(x, y).red = 0
                    collage.get_pixel(x, y).green = 0
                    collage.get_pixel(x, y).blue = 0
                # Bottom border
                elif y >= thickness * 2 + image1.height + image3.height:
                    collage.get_pixel(x, y).red = 0
                    collage.get_pixel(x, y).green = 0
                    collage.get_pixel(x, y).blue = 0
                # Middle horizontal border
                elif thickness + image1.height <= y < thickness * 2 + image1.height:
                    collage.get_pixel(x, y).red = 0
                    collage.get_pixel(x, y).green = 0
                    collage.get_pixel(x, y).blue = 0
                # Left border
                elif x < thickness:
                    collage.get_pixel(x, y).red = 0
                    collage.get_pixel(x, y).green = 0
                    collage.get_pixel(x, y).blue = 0
                # Right border
                elif x >= thickness * 2 + image1.width + image2.width:
                    collage.get_pixel(x, y).red = 0
                    collage.get_pixel(x, y).green = 0
                    collage.get_pixel(x, y).blue = 0
                # Middle vertical border
                elif thickness + image1.width <= x < thickness * 2 + image1.width:
                    collage.get_pixel(x, y).red = 0
                    collage.get_pixel(x, y).green = 0
                    collage.get_pixel(x, y).blue = 0
                # image1
                elif (thickness <= x < thickness + image1.width and thickness <= y < thickness + image1.height):
                    collage.get_pixel(x, y).red = image1.get_pixel(x - thickness, y - thickness).red
                    collage.get_pixel(x, y).green = image1.get_pixel(x - thickness, y - thickness).green
                    collage.get_pixel(x, y).blue = image1.get_pixel(x - thickness, y - thickness).blue
                # image2
                elif (thickness * 2 + image1.width <= x < thickness * 2 + image1.width + image2.width and thickness <= y < thickness + image2.height):
                    collage.get_pixel(x, y).red = image2.get_pixel(x - (thickness * 2 + image1.width), y - thickness).red
                    collage.get_pixel(x, y).green = image2.get_pixel(x - (thickness * 2 + image1.width), y - thickness).green
                    collage.get_pixel(x, y).blue = image2.get_pixel(x - (thickness * 2 + image1.width), y - thickness).blue
                # image3
                elif (thickness <= x < thickness + image3.width and thickness * 2 + image1.height <= y < thickness * 2 + image1.height + image3.height):
                    collage.get_pixel(x, y).red = image3.get_pixel(x - thickness, y - (thickness * 2 + image1.height)).red
                    collage.get_pixel(x, y).green = image3.get_pixel(x - thickness, y - (thickness * 2 + image1.height)).green
                    collage.get_pixel(x, y).blue = image3.get_pixel(x - thickness, y - (thickness * 2 + image1.height)).blue
                # image4
                elif (thickness * 2 + image1.width <= x < thickness * 2 + image1.width + image4.width and thickness * 2 + image1.height <= y < thickness * 2 + image1.height + image4.height):
                    collage.get_pixel(x, y).red = image4.get_pixel(x - (thickness * 2 + image1.width), y - (thickness * 2 + image1.height)).red
                    collage.get_pixel(x, y).green = image4.get_pixel(x - (thickness * 2 + image1.width), y - (thickness * 2 + image1.height)).green
                    collage.get_pixel(x, y).blue = image4.get_pixel(x - (thickness * 2 + image1.width), y - (thickness * 2 + image1.height)).blue

    collage.save(output_file)


def detect_green(pixel, factor, threshold):
    average = (pixel.red + pixel.green + pixel.blue) / 3
    if pixel.green >= factor * average and pixel.green > threshold:
        return True
    else:
        return False


def greenscreen(foreground, background, output_file, threshold, factor):
    threshold = int(threshold)
    factor = float(factor)
    foreground = Image(foreground)
    background = Image(background)
    final = Image.blank(background.width,background.height)
    for y in range(background.height):
        for x in range(background.width):
            fp = final.get_pixel(x,y)
            bp = background.get_pixel(x,y)
            fp.red = bp.red
            fp.green = bp.green
            fp.blue = bp.blue

    for y in range(foreground.height):
        for x in range(foreground.width):
            fp = foreground.get_pixel(x, y)
            if not detect_green(fp, factor, threshold):
                np = final.get_pixel(x,y)
                np.red = fp.red
                np.green = fp.green
                np.blue =fp.blue
    final.save(output_file)

    
# def greenscreen(image1, image2, output_file, threshold, factor):
#     threshold = int(threshold)
#     factor = float(factor)
#     image1 = Image(image1)
#     image2 = Image(image2)
#     greenscreen_image = Image.blank(image1.width, image1.height)
#     for y in range(greenscreen_image.height):
#         for x in range(greenscreen_image.width):
#             pixel1 = image1.get_pixel(x, y)
#             pixel2 = image2.get_pixel(x, y)
                
                
#     greenscreen_image.get_pixel(x, y).blue = pixel1.blue

    

#     greenscreen_image.save(output_file)

    
def main():
    if check_flag(given_flag):
        image = Image(sys.argv[2])
        if given_flag == "-d": # should have 1 argument <input file>
            if len(sys.argv[2:]) > 1:
                raise ValueError("Too many arguments")
            elif len(sys.argv[2:]) < 1:
                raise ValueError("Not enough arguments")
            elif len(sys.argv[2:]) == 1:
                display_image(image)

        elif given_flag == "-g": # should have 2 arguments <input file> <output file>
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

        elif given_flag == "-k": # should have 3 arguments <input file> <output file> <percent>
            if len(sys.argv[2:]) > 3:
                raise ValueError("Too many arguments")
            elif len(sys.argv[2:]) < 3:
                raise ValueError("Not enough arguments")
            elif len(sys.argv[2:]) == 3:
                apply_darken(image, sys.argv[3], sys.argv[4])

        elif given_flag == "-b": # should have 6 arguments <input file> <output file> <thickness> <red> <green> <blue>
            if len(sys.argv[2:]) > 6:
                raise ValueError("Too many arguments")
            elif len(sys.argv[2:]) < 6:
                raise ValueError("Not enough arguments")
            elif len(sys.argv[2:]) == 6:    
                apply_borders(image, sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])

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

        elif given_flag == "-c": # should have 6 arguments <image 1> <image 2> <image 3> <image 4> <output image> <border thickness>
            if len(sys.argv[2:]) > 6:
                raise ValueError("Too many arguments")
            elif len(sys.argv[2:]) < 6:
                raise ValueError("Not enough arguments")
            elif len(sys.argv[2:]) == 6:
                create_collage(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])

        elif given_flag == "-y": # should have 5 arguments <foreground image> <background image> <output file> <threshold> <factor>
            if len(sys.argv[2:]) > 5:
                raise ValueError("Too many arguments")
            elif len(sys.argv[2:]) < 5:
                raise ValueError("Not enough arguments")
            elif len(sys.argv[2:]) == 5:
                greenscreen(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

    else:
        raise ValueError("Invalid flag")


if __name__ == "__main__":
    main()