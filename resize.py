from PIL import Image
import os

input_path = "C:\\Users\\Dotun Local\\Downloads\\spacepixels\\spacepixels-0.1.0\\asteroid_tiny.png"

output_path = "C:\\Users\\Dotun Local\\Documents\\9.660Sprites\\"

""" for (dirpath, dirnames, filenames) in os.walk(input_path):
    for filename in filenames:
        if filename.endswith(".png"):
            name_list = filename.split("_")
            if "blue" in name_list:
                size = 25, 25
            else:
                size = 35,25
            outfile = filename.split(".")[0] + "_resize.png"
            try:
                im = Image.open(input_path + "\\" + filename)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(output_path + "\\" + outfile)
            except IOError:
                print("%s done goofed" % filename) """

""" size = 15, 15
outfile = "asteroid.png"
im = Image.open(input_path)
im.thumbnail(size, Image.ANTIALIAS)
im.save(output_path + "\\" + outfile) """

input_path = "C:\\Users\\Dotun Local\\Downloads\\spacepixels\\spacepixels-0.1.0\\lasers"

size = 10,9
for (dirpath, dirnames, filenames) in os.walk(input_path):
    for filename in filenames:
        if filename.endswith(".png"):
            outfile = filename.split(".")[0] + "_resize.png"
            try:
                im = Image.open(input_path + "\\" + filename)
                im.thumbnail(size, Image.ANTIALIAS)
                im.save(output_path + "\\" + outfile)
            except IOError:
                print("%s done goofed" % filename)