import argparse
import pikepdf

def unlock(pdf_path):
    with pikepdf.open(pdf_path) as pdf:
        pdf.save(pdf_path.replace(".pdf", "_unlocked.pdf"))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-path", help="Path to the PDF file to unlock")

    args = parser.parse_args()

    if args.pdf_path:
        unlock(args.pdf_path)
    else:
        print("Please provide the path to the PDF file to unlock")

if __name__ == "__main__":
    main()
