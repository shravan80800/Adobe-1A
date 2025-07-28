import fitz  # PyMuPDF

def extract_pdf_content(file_path):
    doc = fitz.open(file_path)
    blocks = []
    for page_num, page in enumerate(doc):
        for block in page.get_text("dict")["blocks"]:
            if "lines" in block:
                text = ""
                for line in block["lines"]:
                    for span in line["spans"]:
                        text += span["text"] + " "
                text = text.strip()
                if text:
                    blocks.append({
                        "text": text,
                        "font_size": span["size"],
                        "font": span["font"],
                        "bbox": block["bbox"],
                        "page": page_num
                    })
    return blocks
