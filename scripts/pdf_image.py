import os
import fitz  # PyMuPDF
import os

def convert_pdf_to_images(pdf_path):
    # Open the PDF file using PyMuPDF
    pdf = fitz.open(pdf_path)
    images = []

    # Iterate over each page in the PDF
    for page_num in range(len(pdf)):
        # Get the page
        page = pdf[page_num]

        # Render page to an image (pix) object
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")
        images.append(img_data)

    pdf.close()
    return images


def save_images_to_files(images, directory="/content/data"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_paths = []
    for i, img_data in enumerate(images):
        file_path = f"{directory}/page_{i}.png"
        # Since image data is in bytes, it can be directly written to a file in 'wb' mode
        with open(file_path, 'wb') as f:
            f.write(img_data)
        file_paths.append(file_path)
    return file_paths

