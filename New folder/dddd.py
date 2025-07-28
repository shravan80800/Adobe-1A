import pandas as pd
import random
import numpy as np

n = 50000
rows = []
labels = ["Title", "H1", "H2", "H3", "Other"]

# Simple templates for each language
langs = [
    {
        "code": "en",
        "title": "Chapter {N}: Introduction to Something",
        "h1": "{N}. Major Section",
        "h2": "{N}.{M} Subsection",
        "h3": "{N}.{M}.{K} Nested Section",
        "body": "This is an example sentence in English about a certain topic."
    },
    {
        "code": "fr",
        "title": "Chapitre {N} : Introduction à quelque chose",
        "h1": "{N}. Section principale",
        "h2": "{N}.{M} Sous-section",
        "h3": "{N}.{M}.{K} Section imbriquée",
        "body": "Ceci est une phrase d'exemple en français sur un certain sujet."
    },
    {
        "code": "hi",
        "title": "अध्याय {N}: किसी विषय का परिचय",
        "h1": "{N}. मुख्य अनुभाग",
        "h2": "{N}.{M} उप अनुभाग",
        "h3": "{N}.{M}.{K} नेस्टेड अनुभाग",
        "body": "यह किसी विषय के बारे में हिंदी में एक उदाहरण वाक्य है।"
    },
    {
        "code": "es",
        "title": "Capítulo {N}: Introducción a algo",
        "h1": "{N}. Sección principal",
        "h2": "{N}.{M} Subsección",
        "h3": "{N}.{M}.{K} Sección anidada",
        "body": "Esta es una frase de ejemplo en español sobre un tema determinado."
    },
    {
        "code": "de",
        "title": "Kapitel {N}: Einführung in etwas",
        "h1": "{N}. Hauptabschnitt",
        "h2": "{N}.{M} Unterabschnitt",
        "h3": "{N}.{M}.{K} Verschachtelter Abschnitt",
        "body": "Dies ist ein Beispielsatz auf Deutsch zu einem bestimmten Thema."
    }
]

for i in range(n):
    label = random.choices(labels, weights=[0.03, 0.12, 0.2, 0.15, 0.5])[0]
    lang = random.choice(langs)
    N = random.randint(1, 20)
    M = random.randint(1, 15)
    K = random.randint(1, 12)
    if label == "Title":
        text = lang["title"].format(N=N)
        font_size = random.uniform(20, 26)
        bold = 1
    elif label == "H1":
        text = lang["h1"].format(N=N)
        font_size = random.uniform(16, 20)
        bold = random.choice([1, 1, 0])
    elif label == "H2":
        text = lang["h2"].format(N=N, M=M)
        font_size = random.uniform(14, 18)
        bold = random.choice([1, 0])
    elif label == "H3":
        text = lang["h3"].format(N=N, M=M, K=K)
        font_size = random.uniform(12, 16)
        bold = random.choice([1, 0, 0])
    else:
        text = lang["body"]
        font_size = random.uniform(10, 14)
        bold = random.choice([0, 0, 1])
    italic = random.choice([0, 0, 1])
    y_position = random.uniform(50, 800)
    page_number = random.randint(0, 40)
    rows.append({
        "text": text,
        "font_size": round(font_size, 2),
        "bold": bold,
        "italic": italic,
        "y_position": round(y_position, 2),
        "page_number": page_number,
        "label": label,
        "lang": lang["code"]
    })

df = pd.DataFrame(rows)
df.to_csv("sample_training_data.csv", index=False)
print("✅ Generated sample_training_data_multilingual.csv with 50,000 entries.")
