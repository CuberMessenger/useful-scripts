import os
import qrcode

def main():
    message = "Elohim lies about the tower."
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        border=0
    )

    qr.add_data(message)

    qr.make(fit=True)

    image = qr.make_image(fill_color=(0, 0, 0), back_color=(255, 255, 255))
    image.save("qr.png")

if __name__ == "__main__":
    main()
