# summarizer.py
from transformers import pipeline
import re

# Inicializa el modelo de resumen
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text):
    """Limpia el texto eliminando espacios extra y caracteres raros"""
    return re.sub(r'\s+', ' ', text).strip()

def summarize_articles(articles):
    """
    Recibe una lista de artículos con 'title' y 'content'
    Devuelve un resumen narrativo de cada uno
    """
    summaries = []
    for article in articles:
        title = article['title']
        content = article['content']

        # Limpieza y acortar si es muy largo
        full_text = clean_text(content)
        if len(full_text) > 1024:
            full_text = full_text[:1024]

        try:
            result = summarizer(full_text, max_length=120, min_length=60, do_sample=False)
            summary = result[0]['summary_text']
            summaries.append(f"🔹 {title}\n   {summary}\n")
        except Exception as e:
            print(f"❌ Error resumiendo '{title}': {str(e)}")
            summaries.append(f"🔹 {title}\n   No se pudo generar un resumen automático.\n")
    
    return "\n".join(summaries)
