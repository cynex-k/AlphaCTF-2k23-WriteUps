# HelloPNG

**`Author:`** [Cynex](https://github.com/cynex-k)

## Description:
>I build this image from scratch and applied a FILTER
  I bet you know PNG better than me
  can you reveal the secret from this ......

## Attachment:
![Challenge.png](../Challenge.png)

## Solution:
If we read the description carefully we see this keywords `FILTER` ,`PNG`
a small search about filter in png 
I found in this blog: [HelloPNG](https://www.da.vidbuchanan.co.uk/blog/hello-png.html)

The idea of [filtering](https://www.w3.org/TR/2022/WD-png-3-20221025/#9Filters) is to make the image data more readily compressible.

You may recall that the `IHDR` chunk has a "Filter method" field. The only specified filter method is method 0, called "adaptive filtering" (the others are reserved for future revisions of the PNG format).

In [Adaptive Filtering](https://www.w3.org/TR/2022/WD-png-3-20221025/#9Filter-types), each row of pixels is prefixed by a single byte that describes the Filter Type used for that particular row. There are 5 possible Filter Types, but for now, we're only going to care about type 0, which means "None".

If we had a tiny 3x2 pixel image comprised of all-white pixels, the filtered image data would look something like this: (byte values expressed in decimal)

0   255 255 255  255 255 255  255 255 255
0   255 255 255  255 255 255  255 255 255

I've added whitespace and a newline to make it more legible. The two zeroes at the start of each row encode the filter type, and the "255 255 255"s each encode a white RGB pixel (with each sub-pixel at maximum brightness).

This is the simplest possible way of "filtering" PNG image data. Of course, it doesn't do anything especially useful since we're only using the "None" filter, but it's still a requirement to have a valid PNG file
so I write a small script to extract the filter bit from idat chunk
```python
import png

img = open('Challenge.png', 'rb')
img = png.Reader(file=img)
img.preamble()


def iteridat(reader: png.Reader, lenient=False):
    """Iterator that yields all the ``IDAT`` chunks as strings."""
    while True:
        type, data = reader.chunk(lenient=lenient)
        if type == b'IEND':
            break
        if type != b'IDAT':
            continue
        yield data


raw = png.decompress(iteridat(img))
a, filters = bytearray(), []
for some_bytes in raw:
    a.extend(some_bytes)
    while len(a) >= img.row_bytes + 1:
        filters.append(a[0])
        scanline = a[1: img.row_bytes + 1]
        del a[: img.row_bytes + 1]

filter_str = ''.join([str(i) for i in filters])
for i in range(0,len(filter_str),7):
    print(chr(int(filter_str[i:i+7],2)),end="")
```

## Flag
`AlphaCTF{f1Lter5_b1T_fun}`  
