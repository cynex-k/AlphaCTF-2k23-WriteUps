import qrcode
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_Q,
    box_size=10,
    border=4,
    mask_pattern=1,
)
qr.add_data('Qr_D3c0d3_!')
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("Qr_Q.png")



'''
               |    Q    |    r    |    _    |    D    |    3    |    c    |    0    |    d    |    3    |    _    |    !    |
 0100 0000 1011 0101 0001 0111 0010 0101 1111 0100 0100 0011 0011 0110 0011 0011 0000 0110 0100 0011 0011 0101 1111 0010 0001 0000
|    40   |    B5   |    17   |   25    |   F4    |   43    |    36   |   33    |   06    |   43    |   35    |    F2   |   10    |
                                  X                    X

from reedsolo import RSCodec, ReedSolomonError
rsc = RSCodec(13)
rsc.decode(b'@\xb5\x17X\xf4X63\x06C5\xf2\x10\xbd\x05X\xdc\x138XeX\x16iX\xa5')                                  
'''