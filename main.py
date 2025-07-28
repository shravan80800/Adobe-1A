import os
import json
from extract_pdf_lines import extract_pdf_lines
from utils.classifier import classify_headings
from utils.postprocess import build_outline_json

INPUT_DIR = "input"
OUTPUT_DIR = "output"
MODEL_PATH = "model/paraphrase-multilingual-MiniLM-L12-v2"
CLF_PATH = "model/clf.pkl"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_all_pdfs():
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf"):
            print(f"\n📄 Processing: {filename}")
            input_path = os.path.join(INPUT_DIR, filename)

            # Extract features from the PDF
            lines = extract_pdf_lines(input_path)

            # Classify headings (H1, H2, H3, etc.)
            predictions = classify_headings(lines, model_path=MODEL_PATH, clf_path=CLF_PATH)

            # Display classification summary
            for i, (line, pred) in enumerate(zip(lines, predictions)):
                print(f"{i:03d}: [{pred}] {line['text']} (pg {line['page']})")

            # Generate structured JSON output
            output_json = build_outline_json(filename, lines, predictions)
            output_path = os.path.join(OUTPUT_DIR, filename.replace(".pdf", ".json"))

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(output_json, f, indent=2, ensure_ascii=False)

            print(f"✅ JSON saved to: {output_path}")

if __name__ == "__main__":
    process_all_pdfs()
