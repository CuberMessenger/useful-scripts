import os
import qrcode
import numpy as np

from PIL import Image

def main():
    message = ""
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        border=0
    )

    qr.add_data(message)

    qr.make(fit=True)

    image = qr.make_image(fill_color=(219, 105, 44), back_color=(248, 234, 225))
    image.save("qr.png")

if __name__ == "__main__":
    main()
