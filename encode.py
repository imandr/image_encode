import sys, getopt
from zlib import adler32
from PIL import Image
from rnd import Generator, sample

Usage = """
python encode <text file> <password> <input image file> <output image file>
"""

def cbits(c):
    n = ord(c)
    out = []
    for _ in range(8):
        out.append(n&1)
        n >>= 1
    return out
    
def tobin(x, n):
    out = []
    for _ in range(n):
        out.append(x&1)
        x >>= 1
    return out
    
def bits(text):
    if isinstance(text, str):
        text = text.encode("utf-8")
    out = []
    for c in text:
        n = c
        cbits = []
        for _ in range(8):
            cbits.append(n&1)
            n >>= 1
        #print("cbits:", cbits)
        out += cbits
    return out

def flip_pixels(image, bits, inx):
    dimx, dimy = image.size
    pixels = image.load()
    for j, (p, i) in enumerate(zip(bits, inx)):
        row = i//dimx
        col = i%dimx
        rgb = pixels[col, row]
        r,g,b = rgb
        parity = (r^(g^b))&1
        if parity != p:
            rgb = list(rgb)
            ic = i%3
            c = rgb[ic]
            rgb[ic] = c ^ 1
            pixels[col, row] = tuple(rgb)
        
def create_pixel_map(gen, image, length):
    dimx, dimy = image.size
    npixels = dimx*dimy
    pixel_list = list(range(npixels))
    
    length_inx = sample(gen, pixel_list, 32)

    for inx in length_inx:
        pixel_list.remove(inx)

    text_inx = sample(gen, pixel_list, length*8)
    return length_inx, text_inx


text_file, password, inp_image_file, out_image_file = sys.argv[1:]

text = open(text_file, "rb").read()

image = Image.open(inp_image_file)
gen = Generator(password)
length_inx, text_inx = create_pixel_map(gen, image, len(text))
#print("pixel map:", length_inx, text_inx[:20])


length_bits = tobin(len(text), 32)
text_bits = bits(text)

flip_pixels(image, length_bits, length_inx)
flip_pixels(image, text_bits, text_inx)

image.save(out_image_file, "png")
     









