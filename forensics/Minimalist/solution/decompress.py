import zlib 
from PIL import Image

# read the IDAT chunk 
chunk = open("chall.bin","rb").read()

# extract the size of the chunk
size = int(chunk[:4].hex(),16)

# extrcat the chunk data
chunk_data = chunk[8:size+8]

# decompress the data with zlib
uncompres = zlib.decompress(chunk_data)

# Remove the filter bit 
rgb = b''
j =0
for i in range(len(uncompres)):
    if i == j*463:
        j+=1
    else:
        rgb +=int.to_bytes(uncompres[i])

# Prepare the RGB values
pixels = []
for i in range(0,len(rgb),3):
    pix = (int(rgb[i:i+1].hex(),16),int(rgb[i+1:i+2].hex(),16),int(rgb[i+2:i+3].hex(),16))
    pixels.append(pix)


# Build the image
width = 154
height = 151
img = Image.new('RGB', (width, height))

# embed the pixels value inside the image
img.putdata(pixels)

# Save the image to a file
img.save('my_image.png')
