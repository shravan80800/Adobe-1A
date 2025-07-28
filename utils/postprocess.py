import json
import re

def is_valid_heading(text):
    """
    Returns True if text is a valid heading: must include at least one alphabet
    and not be just numbers, dots, or short junk like "1.", "2.1", etc.
    """
    txt = text.strip()
    # Too short or no letters
    if len(txt) < 4 or not re.search(r"[A-Za-z]", txt):
        return False
    # Only digits, dots, or whitespace
    if re.fullmatch(r"[\d\.\s]+", txt):
        return False
    return True


def build_outline_json(filename, lines, predictions):
    outline = []

    # Extract title as the largest font on page 0
    page0 = [l for l in lines if l.get("page", -1) == 0]
    title = None
    if page0:
        top = max(page0, key=lambda l: (l.get("font_size", 0), -l.get("y_position", 0)))
        title = top.get("text", filename.replace(".pdf", ""))

    # Build outline list
    for line, pred in zip(lines, predictions):
        label = pred if pred in ("H1", "H2", "H3") else line.get("label", "Other")
        if label in ("H1", "H2", "H3") and is_valid_heading(line.get("text", "")):
            outline.append({
                "text": line.get("text", ""),
                "level": label,
                "page": line.get("page", 0)
            })

    data = {
        "title": title or filename.replace(".pdf", ""),
        "outline": outline
    }

    # Write JSON file
    out_path = f"output/{filename.replace('.pdf', '.json')}"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return data
