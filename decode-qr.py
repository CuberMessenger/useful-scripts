import argparse
import sys
from PIL import Image
import pyperclip
import requests
from io import BytesIO
from pyzbar.pyzbar import decode

def decode_qr_from_image(image):
    decoded_objects = decode(image)
    if decoded_objects:
        return decoded_objects[0].data.decode()
    else:
        return "No QR code detected."

def get_image_from_clipboard():
    try:
        image = Image.open(pyperclip.paste())
        return image
    except Exception as e:
        print("Failed to read from clipboard:", e)
        sys.exit(1)

def get_image_from_path(path):
    if path.startswith('http://') or path.startswith('https://'):
        try:
            response = requests.get(path)
            image = Image.open(BytesIO(response.content))
            return image
        except Exception as e:
            print("Failed to load image from URL:", e)
            sys.exit(1)
    else:
        try:
            image = Image.open(path)
            return image
        except Exception as e:
            print("Failed to load image from path:", e)
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Decode a QR code from an image.')
    parser.add_argument('--path', type=str, help='Path to the image file or URL containing the QR code.')
    args = parser.parse_args()

    if args.path:
        image = get_image_from_path(args.path)
    else:
        image = get_image_from_clipboard()

    result = decode_qr_from_image(image)
    if result:
        print("Decoded QR code:", result)
    else:
        print("No QR code could be decoded.")

if __name__ == "__main__":
    main()
