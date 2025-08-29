# summarizer.py
from transformers import pipeline
import re

# Inicializa el modelo
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def summarize_articles(articles):
    summaries = []
    for article in articles:
        title = article['title']
        content = article['content']  # ✅ Ahora usa 'content', no 'summary'

        # Limpieza
        full_text = clean_text(content)
        if len(full_text) > 1024:
            full_text = full_text[:1024]

        try:
            result = summarizer(full_text, max_length=120, min_length=60, do_sample=False)
            summary = result[0]['summary_text']
            summaries.append(f"🔹 {title}\n   {summary}\n")
        except Exception as e:
            print(f"❌ Error resumiendo {title}: {str(e)}")
            summaries.append(f"🔹 {title}\n   No se pudo resumir.\n")
    
    return "\n".join(summaries)
