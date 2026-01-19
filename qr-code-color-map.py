import os
import qrcode

def main():
    message = "Nha Nheo Nhen is throwing the ball to the back of the toilet."
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=2,
    )

    qr.add_data(message)

    qr.make(fit=True)

    image = qr.make_image(fill_color=(255, 195, 62), back_color=(219, 101, 56))
    image.save("qr.png")

if __name__ == "__main__":
    main()
