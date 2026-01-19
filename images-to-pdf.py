import os
import tqdm
import argparse
import requests
import multiprocessing

from PIL import Image
from fpdf import FPDF


def load_image_paths(folder):
    image_paths = [
        os.path.join(folder, name)
        for name in os.listdir(folder)
        if name.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif", "webp"))
    ]

    return image_paths


def load_image(path):
    try:
        if path.startswith("http://") or path.startswith("https://"):
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"
            }
            image = Image.open(
                requests.get(path, stream=True, headers=headers).raw
            ).convert("RGB")
        else:
            image = Image.open(path).convert("RGB")
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        return None

    return image


def load_images(paths):
    paths.sort()

    cpu_count = multiprocessing.cpu_count()
    with multiprocessing.Pool(cpu_count) as pool:
        images = list(
            tqdm.tqdm(
                pool.imap(load_image, paths),
                total=len(paths),
                desc="Loading images...",
            )
        )

    return images


def images_to_pdf(image_paths, pdf_path):
    images = load_images(image_paths)
    images = [image for image in images if image is not None]
    max_width = max(image.size[0] for image in images)

    pdf = FPDF(unit="pt")

    for image in tqdm.tqdm(images, desc="Converting to PDF..."):
        width, height = image.size

        if width != max_width:
            ratio = max_width / width

            width = max_width
            height = int(round(height * ratio))

            image = image.resize((width, height), Image.Resampling.LANCZOS)

        pdf.add_page(format=(width, height), orientation="P")
        pdf.image(image, x=0, y=0, w=width, h=height)

    pdf.output(pdf_path)
    print(f"PDF saved to {pdf_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert image(s) to a PDF losslessly."
    )
    parser.add_argument("--name", help="Name of the PDF file", default="output")
    parser.add_argument("--path", type=str, help="Path to the image")
    parser.add_argument("--folder", type=str, help="Folder contains a batch of images")
    parser.add_argument(
        "--urls", nargs="+", help="URLs of the images to download and convert to PDF"
    )
    args = parser.parse_args()

    if args.path is not None:
        image_paths = [args.path]
        save_folder = os.path.dirname(args.path)
        # save to the source location
        pdf_path = os.path.join(save_folder, f"{args.name}.pdf")
    elif args.folder is not None:
        image_paths = load_image_paths(args.folder)
        # save to the image folder
        pdf_path = os.path.join(args.folder, f"{args.name}.pdf")
    elif args.urls is not None:
        image_paths = args.urls
        # save to the current directory
        pdf_path = f"{args.name}.pdf"
    else:
        print("Please provide either a file path or a folder containing images.")
        exit(1)

    images_to_pdf(image_paths, pdf_path)


if __name__ == "__main__":
    main()
