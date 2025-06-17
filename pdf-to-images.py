import os
import sys
import tqdm
import shutil
import argparse
import multiprocessing

from pdf2image import convert_from_path


def crop_image(image, crop_ratio, target_ratio):
    # direct crop
    width, height = image.size

    horizontal_crop = int(round((width * crop_ratio[0]) / 2))
    vertical_crop = int(round((height * crop_ratio[1]) / 2))

    left = horizontal_crop
    right = width - horizontal_crop
    upper = vertical_crop
    lower = height - vertical_crop

    image = image.crop((left, upper, right, lower))

    # additional crop to target ratio
    if target_ratio > 0:
        width, height = image.size
        current_ratio = height / width

        if current_ratio > target_ratio:
            vertical_crop = int(round((height - width * target_ratio) / 2))

            left = 0
            right = width
            upper = vertical_crop
            lower = height - vertical_crop
            
        elif current_ratio < target_ratio:
            horizontal_crop = int(round((width - height / target_ratio) / 2))

            left = horizontal_crop
            right = width - horizontal_crop
            upper = 0
            lower = height

        else:
            pass

        image = image.crop((left, upper, right, lower))

    return image

def convert_page(parameters):
    page, path, dpi, crop_ratio, target_ratio = parameters
    page = crop_image(page, crop_ratio, target_ratio)
    page.save(path, dpi=(dpi, dpi))


def pdf_to_images(pdf_path, output_folder, dpi, format, crop_ratio, target_ratio):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)

    cpu_count = multiprocessing.cpu_count()

    print("Loading PDF ......")
    try:
        pages = convert_from_path(pdf_path, dpi=dpi, thread_count=cpu_count)
    except Exception as e:
        print(f"Error converting PDF: {e}", file=sys.stderr)
        sys.exit(1)

    image_paths = [
        os.path.join(output_folder, f"page_{i:03d}.{format.lower()}")
        for i in range(1, len(pages) + 1)
    ]

    def convert_page_arguments():
        for i, page in enumerate(pages):
            yield page, image_paths[i], dpi, crop_ratio, target_ratio

    with multiprocessing.Pool(cpu_count) as pool:
        list(
            tqdm.tqdm(
                pool.imap(
                    convert_page,
                    convert_page_arguments(),
                ),
                total=len(pages),
                desc="Converting PDF pages to images ......",
            )
        )


def main():
    parser = argparse.ArgumentParser(
        description="Convert each page of a PDF to images."
    )
    parser.add_argument("--path", help="Path to the input PDF file.")
    parser.add_argument(
        "--folder",
        default="output",
        help="Output folder where images will be saved.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="Dots per inch for the output images.",
    )
    parser.add_argument(
        "--format",
        type=str,
        default="PNG",
        help="Format of the output images (PNG or JPEG).",
    )
    parser.add_argument(
        "--horizontal-crop",
        type=float,
        default=0.0,
        help="Horizontal crop ratio (0.0 to 1.0) for the output images.",
    )
    parser.add_argument(
        "--vertical-crop",
        type=float,
        default=0.0,
        help="Vertical crop ratio (0.0 to 1.0) for the output images.",
    )
    parser.add_argument(
        "--ratio",
        type=float,
        default=297 / 210,  # Default A4 aspect ratio
        help="Target height / width ratio for the output images. Zero means no additional cropping.",
    )
    args = parser.parse_args()

    pdf_to_images(
        args.path,
        args.folder,
        args.dpi,
        args.format,
        (args.horizontal_crop, args.vertical_crop),
        args.ratio,
    )


if __name__ == "__main__":
    main()
