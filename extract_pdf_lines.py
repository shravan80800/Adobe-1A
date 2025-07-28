import fitz  # PyMuPDF
import pandas as pd

def extract_pdf_lines(pdf_path, csv_path=None):
    doc = fitz.open(pdf_path)
    lines = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            if not text.strip():
                continue
            # Split into individual lines
            for line_text in text.split("\n"):
                line_text = line_text.strip()
                if not line_text:
                    continue
                # Try to find matching font info
                font_size = 12
                bold = 0
                italic = 0
                found = False
                spans = page.get_text("dict")["blocks"]
                for block in spans:
                    if "lines" not in block:
                        continue
                    for l in block["lines"]:
                        for span in l["spans"]:
                            if line_text in span["text"]:
                                font_size = span["size"]
                                bold = int("Bold" in span["font"])
                                italic = int("Italic" in span["font"])
                                found = True
                                break
                        if found:
                            break
                    if found:
                        break
                lines.append({
                    "text": line_text,
                    "font_size": font_size,
                    "bold": bold,
                    "italic": italic,
                    "y_position": y0,
                    "page": page_num
                })
    df = pd.DataFrame(lines)
    if csv_path is not None:
        df.to_csv(csv_path, index=False)
        print(f"✅ Extracted {len(df)} lines to {csv_path}")
    return df.to_dict(orient="records")

# Example usage:
# lines = extract_pdf_lines("file02.pdf")             # returns a list of dicts
# lines = extract_pdf_lines("file02.pdf", "lines.csv") # also writes to CSV
