# 🧠 PDF Outline Extractor & Classifier

> Extracts structured outlines (Title, H1, H2, H3, Other) from PDFs using multilingual sentence embeddings and XGBoost — **fully offline, Docker-ready, and easy to use**.

<p align="center">
  <img src="https://img.shields.io/badge/Offline--Ready-✅-brightgreen" />
  <img src="https://img.shields.io/badge/Docker-Supported-blue" />
  <img src="https://img.shields.io/badge/Pretrained%20Model-Included-success" />
  <img src="https://img.shields.io/badge/Python-3.10+-blue" />
</p>

---

## ✨ Features

- ✅ **Multilingual** sentence embedding model (`paraphrase-multilingual-MiniLM`)
- 🔢 **Heading hierarchy prediction** (Title, H1, H2, H3, Other) via XGBoost
- 🐳 **Docker-ready** — run in one command
- 📦 **Pretrained model included** — no internet needed
- 📤 **Structured JSON output** for easy integration

---

## 📂 Project Structure

```
.
├── model/                          # Pretrained model and components
│   ├── clf.pkl                     # Trained XGBoost classifier
│   ├── label_encoder.pkl           # Label encoder for heading labels
│   ├── paraphrase-multilingual-*   # Sentence Transformer model
│   └── model_backup.zip            # Full model backup (optional restore)
├── input/                          # Place input PDFs here
├── output/                         # Output folder for JSON results
├── main.py                         # Main pipeline runner
├── extract_pdf_lines.py            # PDF text + layout extractor
├── train_classifier.py             # Retrain model on custom data
├── predict_outline.py              # Test model on CSV data
├── downloadmodel.py                # Model downloader (optional)
├── requirements.txt                # Dependencies
├── Dockerfile                      # Docker image setup
└── utils/
    ├── classifier.py               # classify_headings() function
    └── postprocess.py              # build_outline_json() function
```

---

## 🚀 Quick Start (Docker)

### 🧱 Step 1: Build Docker Image
```bash
docker build -t pdf-outline .
```

### 📥 Step 2: Place PDFs in `input/` Folder
```bash
cp your_pdfs/*.pdf input/
```

### ▶️ Step 3: Run the Pipeline
```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output pdf-outline
```

✅ Output will be saved to `output/` folder in JSON format.

---

## 🔧 Manual Setup (Without Docker)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

<details>
<summary>Or install manually:</summary>

```bash
pip install pandas numpy joblib sentence-transformers xgboost PyMuPDF
```

</details>

### Step 2: Run Full Pipeline
```bash
python main.py
```

---

## 🧠 Model Info

- ✨ Embedding Model: `paraphrase-multilingual-MiniLM-L12-v2`
- 🔍 Classifier: `XGBoost` trained to detect hierarchy (Title → H3)
- 📁 Stored offline inside `model/` directory

### 💾 Model Recovery
If `model/` is missing or corrupted:
```bash
unzip model/model_backup.zip -d model/
```

Restores:
- `clf.pkl`
- `label_encoder.pkl`
- SentenceTransformer model folder

---

## 📊 JSON Output Format

Example structured output:
```json
{
  "filename": "sample.pdf",
  "outline": [
    {
      "label": "Title",
      "text": "Artificial Intelligence",
      "page": 0
    },
    {
      "label": "H1",
      "text": "1. Introduction",
      "page": 1,
      "children": [
        {
          "label": "H2",
          "text": "1.1 Background",
          "page": 1
        }
      ]
    }
  ]
}
```

---

## 🧪 Optional: Retrain the Classifier

### Step 1: Prepare CSV File
Example: `sample_training_data.csv`
| text         | font_size | bold | italic | y_position | page_number | label |
|--------------|-----------|------|--------|------------|-------------|-------|
| Introduction | 18        | 1    | 0      | 125.5      | 0           | H1    |
| What is AI?  | 14        | 1    | 0      | 160.2      | 0           | H2    |

### Step 2: Train New Model
```bash
python train_classifier.py
```

Overwrites:
- `model/clf.pkl`
- `model/label_encoder.pkl`

---

## 🧪 Optional: Test on CSV (Quick Evaluation)

```bash
python predict_outline.py
```

📄 Output: `predicted_output.csv`

---

## ⚙ Utility Scripts

### `utils/classifier.py`
```python
def classify_headings(lines, model_path, clf_path):
    # Accepts line features (layout, font, embedding)
    # Returns predicted heading labels
```

### `utils/postprocess.py`
```python
def build_outline_json(filename, lines, predictions):
    # Builds a nested JSON structure based on heading levels
```

---

## 🐳 Minimal Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
```

---

## 📃 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙌 Credits

- 🧠 [SentenceTransformers](https://www.sbert.net/)
- 🌲 [XGBoost](https://xgboost.ai/)
- 📄 [PyMuPDF](https://pymupdf.readthedocs.io/)

---

## 💬 Feedback & Contributions

Found a bug? Have an idea?  
👉 [Open an Issue](https://github.com/your-repo/issues) or submit a Pull Request!

---
