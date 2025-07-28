import pandas as pd
import re

# Load extracted lines (from previous extraction script)
df = pd.read_csv("file02_lines_for_labeling.csv")

def detect_lang(text):
    """Very basic language detection for demo purposes."""
    text = text.strip()
    if re.search(r"^\d+(\.\d+)*\s+(Chapitre|Introduction|Traduction|Annexe|Sommaire)", text, re.IGNORECASE) or "français" in text.lower():
        return "fr"
    if re.search(r"^\d+(\.\d+)*\s+(Capítulo|Introducción|Sumario|Apéndice)", text, re.IGNORECASE) or "español" in text.lower():
        return "es"
    if re.search(r"^\d+(\.\d+)*\s+(Kapitel|Einleitung|Anhang|Inhalt)", text, re.IGNORECASE) or "deutsch" in text.lower():
        return "de"
    if re.search(r"^\d+(\.\d+)*\s+(अध्याय|परिचय|अनुच्छेद|अनुलग्नक)", text) or "हिंदी" in text:
        return "hi"
    # Otherwise, assume English
    return "en"

def auto_label(row):
    text = str(row["text"]).strip()
    # Title: "Overview" at the top of page
    if text == "Overview":
        return "Title"
    # H3: 1.2.3 ... pattern
    if re.match(r"^[1-9]\.\d+\.\d+\s", text):
        return "H3"
    # H2: 1.2 ... pattern
    if re.match(r"^[1-9]\.\d+\s", text):
        return "H2"
    # H1: 1. ... (not decimal)
    if re.match(r"^[1-9]\.\s", text):
        return "H1"
    # Everything else
    return "Other"

df["label"] = df.apply(auto_label, axis=1)
df["lang"] = df["text"].apply(detect_lang)
df.to_csv("file02_labeled_autogen.csv", index=False)
print("✅ Auto-labeled and added language column: file02_labeled_autogen.csv")
