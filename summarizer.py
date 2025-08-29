# summarizer.py
from transformers import pipeline
import re

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def summarize_articles(articles):
    summaries = []
    for article in articles:
        title = article['title']
        content = article['content']

        # Limpieza y acortar razonablemente
        full_text = clean_text(content)
        if len(full_text) > 1024:
            full_text = full_text[:1024]  # BART maneja bien hasta 1024

        try:
            result = summarizer(
                full_text,
                max_length=150,     # Hasta 150 tokens (frases completas)
                min_length=70,      # Al menos 2-3 frases
                do_sample=False,
                truncation=True     # Asegura manejo seguro
            )
            summary = result[0]['summary_text']
            summaries.append(f"🔹 {title}\n   {summary}\n")
        except Exception as e:
            print(f"❌ Error resumiendo {title}: {str(e)}")
            summaries.append(f"🔹 {title}\n   No se pudo resumir.\n")
    
    return "\n".join(summaries)
