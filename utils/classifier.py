import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
import os
import json
import re

FORBIDDEN_HEADINGS = [
    "version", "copyright", "date", "remarks",
    "page ", "revision history", "international", "may ", "june ", "july ",
    "aug ", "sep ", "oct ", "nov ", "dec ", "jan ", "feb ", "mar ", "apr "
]

def minimalistic_rule_based(text, label):
    text_lc = text.strip().lower()

    # Demote headings if forbidden keywords present
    if any(kw in text_lc for kw in FORBIDDEN_HEADINGS):
        return "Other"

    # Classic numbered headings: prefer H1/H2/H3 if matching patterns (if ML got it wrong)
    if re.match(r"^\d+\.\s+\S+", text) and label != "H1":
        return "H1"
    if re.match(r"^\d+\.\d+\s+\S+", text) and label != "H2":
        return "H2"
    if re.match(r"^\d+\.\d+\.\d+\s+\S+", text) and label != "H3":
        return "H3"

    # Demote headings if they're too short or too long (likely not actual headings)
    if label in ["H1", "H2", "H3", "Title"]:
        if len(text.strip()) < 4 or len(text.strip()) > 80:
            return "Other"
        if text.strip().endswith(('.', ':', ';')):
            return "Other"
    return label

def load_label_encoder(model_dir="model"):
    pkl_path = os.path.join(model_dir, "label_encoder.pkl")
    json_path = os.path.join(model_dir, "label_encoder.json")
    if os.path.exists(pkl_path):
        le = joblib.load(pkl_path)
        return le, le.classes_
    elif os.path.exists(json_path):
        with open(json_path, "r") as f:
            classes = json.load(f)
        idx2class = {i: c for i, c in enumerate(classes)}
        class DummyLE:
            def inverse_transform(self, arr):
                return [idx2class[i] for i in arr]
            @property
            def classes_(self):
                return classes
        return DummyLE(), classes
    else:
        raise FileNotFoundError("No label_encoder.pkl or label_encoder.json found!")

def classify_headings(lines, model_path, clf_path, model_dir="model"):
    # Load models
    model = SentenceTransformer(model_path)
    clf = joblib.load(clf_path)
    le, classes = load_label_encoder(model_dir)

    # Prepare features (robust page number support)
    layout_feats = np.array([
        [
            l["font_size"],
            l["bold"],
            l["italic"],
            l["y_position"],
            l.get("page_number", l.get("page", 0))
        ]
        for l in lines
    ])
    texts = [l["text"] for l in lines]
    embeddings = model.encode(texts, convert_to_tensor=False, normalize_embeddings=True)
    X = np.hstack([embeddings, layout_feats])

    # Predict and decode
    encoded_preds = clf.predict(X)
    decoded_preds = le.inverse_transform(encoded_preds)

    # Minimal rule-based postprocessing
    final_preds = [
        minimalistic_rule_based(text, label)
        for text, label in zip(texts, decoded_preds)
    ]
    return final_preds
