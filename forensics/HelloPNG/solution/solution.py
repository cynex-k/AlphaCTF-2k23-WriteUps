import png

img = open('hello1.png', 'rb')
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