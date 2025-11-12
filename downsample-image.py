import os
import argparse
from PIL import Image, ImageOps


def scale_length(length, scale_factor):
    return int(round(length / scale_factor))


def downsample_image(input_path, output_path, scale_factor, quality):
    image = Image.open(input_path)
    image = ImageOps.exif_transpose(image)
    width, height = image.size

    image = image.resize(
        (scale_length(width, scale_factor), scale_length(height, scale_factor)),
        Image.NEAREST,
    )

    image.save(output_path, quality=quality)


def main():
    parser = argparse.ArgumentParser(
        description="Downsample an image by a given scale factor."
    )
    parser.add_argument("--input", help="Path to the input image file.")
    parser.add_argument("--output", help="Path to save the downsampled image.")
    parser.add_argument(
        "--factor",
        type=float,
        default=2,
        help="Scale factor for downsampling (default: 2).",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=95,
        help="Quality of the saved image (1-100, default: 95).",
    )

    args = parser.parse_args()

    assert os.path.isfile(args.input), "Input file does not exist."
    assert (
        args.factor > 0
    ), "Scale factor must be greater than 0, and greater than 1 usually."
    assert 1 <= args.quality <= 100, "Quality must be between 1 and 100."

    downsample_image(args.input, args.output, args.factor, args.quality)


if __name__ == "__main__":
    main()
