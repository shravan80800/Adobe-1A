
import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer

# Load models
embedder = SentenceTransformer('model/paraphrase-multilingual-MiniLM-L12-v2')
model = joblib.load("model/clf.pkl")

# Load sample input (simulate)
df = pd.read_csv("sample_training_data.csv")
layout_feats = df[['font_size', 'bold', 'italic', 'y_position', 'page_number']].values
text_lines = df['text'].tolist()

# Generate real embeddings
text_embeddings = embedder.encode(text_lines)

# Combine features
X = np.hstack([text_embeddings, layout_feats])

# Predict
preds = model.predict(X)
label_map = {0: "Title", 1: "H1", 2: "H2", 3: "H3", 4: "Other"}
df['predicted_label'] = [label_map[p] for p in preds]

# Save output
df.to_csv("predicted_output.csv", index=False)
print("✅ Prediction complete → predicted_output.csv")
