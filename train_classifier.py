import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib

# Load data
df = pd.read_csv("sample_training_data.csv")

# Embedding model
embedder = SentenceTransformer("model/paraphrase-multilingual-MiniLM-L12-v2")
embeddings = embedder.encode(df["text"].tolist(), convert_to_tensor=False, normalize_embeddings=True)
layout_feats = df[["font_size", "bold", "italic", "y_position", "page_number"]].values
X = np.hstack([embeddings, layout_feats])

# Labels
le = LabelEncoder()
y = le.fit_transform(df["label"])

# Save label encoder as both .pkl and .json for portability
joblib.dump(le, "model/label_encoder.pkl")
import json
with open("model/label_encoder.json", "w") as f:
    json.dump(list(le.classes_), f)

# XGBoost classifier
clf = xgb.XGBClassifier(tree_method="hist", n_jobs=-1, max_depth=5, n_estimators=100)
clf.fit(X, y)

# Save as joblib (Linux pickle) AND XGBoost's native JSON
joblib.dump(clf, "model/clf.pkl")
clf.save_model("model/clf.xgb.json")

print("✅ Model and label encoder saved for AMD64/Linux!")
