import sys, getopt
from zlib import adler32
from PIL import Image
from rnd import Generator, sample

Usage = """
python decode.py <password> <input image file> <output file>
"""

def bits(text):
    out = []
    for c in text:
        n = ord(c)
        for _ in range(8):
            out.append(n&1)
            n >>= 1
    return out

def frombin(bits):
    n = 0
    k = 1
    for b in bits:
        if b:
            n |= k
        k <<= 1
    return n

def read_bits(image, inx):
    out = []
    pixels = image.load()
    for i in inx:
        row = i//dimx
        col = i%dimx
        rgb = pixels[col, row]
        r,g,b = rgb
        parity = (r^(g^b))&1
        out.append(parity)
    return out
    
def bitstotext(bits):
    text = []
    for i in range(0, len(bits), 8):
        cbits = bits[i:i+8]
        #print("cbits:", cbits)
        n = 0
        k = 1
        for b in cbits:
            if b:   n |= k
            k <<= 1
        #print("cbits:", cbits, "  n:", n)
        text.append(n)
    return bytes(text)        

password, image_file, out_file = sys.argv[1:]
password = password.encode("utf-8")
image = Image.open(image_file)
dimx, dimy = image.size
npixels = dimx*dimy
gen = Generator(password)
pixel_list = list(range(npixels))

length_inx = sample(gen, pixel_list, 32)
for inx in length_inx:
    pixel_list.remove(inx)

length_bits = read_bits(image, length_inx)
length = frombin(length_bits)
#print ("length:", length_bits, length)

text_inx = sample(gen, pixel_list, length*8)
#print("text_inx:", text_inx[:20])
text_bits = read_bits(image, text_inx)

#print("bits:", text_bits[:20])
open(out_file, "wb").write(bitstotext(text_bits))
     









