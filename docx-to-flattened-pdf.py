import os
import sys
import win32com.client
import fitz  # PyMuPDF
import random
import string

def generate_password_from_filename(file_path, length=40):
    """Generates a randomized password seeded by the file's name."""
    # Use just the filename (not the full path) for consistent seeding
    base_name = os.path.basename(file_path)
    
    # Seed the random number generator with the filename
    random.seed(base_name)
    
    # Define the pool of characters (letters, numbers, and safe symbols)
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    
    # Generate the password
    password = "".join(random.choice(characters) for _ in range(length))
    
    # Reset the random seed to system time to prevent predictable randomness elsewhere
    random.seed()
    
    return password

def convert_word_to_pdf(doc_path, temp_pdf_path):
    """Uses MS Word engine to export the document to a standard PDF."""
    print("Opening MS Word...")
    word = None
    doc = None
    try:
        word = win32com.client.DispatchEx("Word.Application")
        word.Visible = False
        
        print(f"Loading document: {doc_path}")
        doc = word.Documents.Open(doc_path)
        
        # 17 represents wdFormatPDF
        doc.SaveAs(temp_pdf_path, FileFormat=17)
        print("Successfully exported standard PDF from Word.")
        
    except Exception as e:
        print(f"Error during Word conversion: {e}")
        sys.exit(1)
        
    finally:
        if doc:
            doc.Close(SaveChanges=0)
        if word:
            word.Quit()

def flatten_pdf(input_pdf, output_pdf, dpi=200, owner_pw="admin"):
    """Converts a standard PDF to a compressed image-based PDF and locks it."""
    print(f"Flattening PDF at {dpi} DPI and applying security permissions...")
    try:
        vector_doc = fitz.open(input_pdf)
        flat_doc = fitz.open()

        for page_num in range(len(vector_doc)):
            page = vector_doc.load_page(page_num)
            
            pix = page.get_pixmap(dpi=dpi, alpha=False)
            img_bytes = pix.tobytes("png")
            
            new_page = flat_doc.new_page(width=page.rect.width, height=page.rect.height)
            new_page.insert_image(page.rect, stream=img_bytes)
            
        # SET PERMISSIONS: Allow printing only.
        # This implicitly denies modifying, copying, and annotating.
        perms = fitz.PDF_PERM_PRINT
            
        # Save with compression, encryption, and permissions
        flat_doc.save(
            output_pdf, 
            deflate=True, 
            garbage=3,
            encryption=fitz.PDF_ENCRYPT_AES_256,
            owner_pw=owner_pw,       # Required to enforce permissions
            permissions=perms
        )
        
        vector_doc.close()
        flat_doc.close()
        print(f"Successfully saved secured, flattened PDF to: {output_pdf}")
        
    except Exception as e:
        print(f"Error during PDF flattening: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: flatten_word.exe <path_to_word_doc>")
        sys.exit(1)

    input_file = os.path.abspath(sys.argv[1])
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    base_path = os.path.splitext(input_file)[0]
    temp_pdf = f"{base_path}_temp.pdf"
    final_pdf = f"{base_path}.pdf"
    
    # ---------------------------------------------------------
    # SET YOUR OWNER PASSWORD HERE
    # Viewers will not be prompted for this password to open it, 
    # but they cannot edit the PDF without it.
    # ---------------------------------------------------------
    SECURE_PASSWORD = generate_password_from_filename(input_file, length=40)

    convert_word_to_pdf(input_file, temp_pdf)
    flatten_pdf(temp_pdf, final_pdf, dpi=200, owner_pw=SECURE_PASSWORD)

    if os.path.exists(temp_pdf):
        os.remove(temp_pdf)
        
    print("Process complete!")

"""
uv run --with pywin32 --with pymupdf --with pyinstaller python -m PyInstaller --onefile to-pdf.py
"""