import pdfplumber
import fitz  # PyMuPDF
import os

def pdf_to_html(pdf_path: str, html_path: str, img_dir: str):
    os.makedirs(img_dir, exist_ok=True)
    with pdfplumber.open(pdf_path) as pdf, fitz.open(pdf_path) as doc, open(html_path, 'w') as html_file:
        html_file.write('<html><body>')

        for i, page in enumerate(pdf.pages):
            # Extract and write text
            text = page.extract_text()
            if text:
                html_file.write(f'<p>{text}</p>')

            # Extract and save images using PyMuPDF
            for img in doc.get_page_images(i):
                xref = img[0]
                base_image = doc.extract_image(xref)
                img_path = f'{img_dir}/img_{i}_{xref}.png'
                with open(img_path, "wb") as f:
                    f.write(base_image["image"])

                # Embed the image in HTML
                html_file.write(f'<img src="{img_path}" alt="Page {i}, Image {xref}"><br>')

        html_file.write('</body></html>')

# Example usage
pdf_to_html('book.pdf', 'index.html', 'images')
