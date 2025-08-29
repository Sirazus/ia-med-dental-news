# summarizer.py
# Resumen gratuito con modelo Hugging Face (sin costo)

from transformers import pipeline
import re

# Usamos un modelo ligero especializado en resúmenes
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def clean_text(text):
    return re.sub(r'\s+', ' ', text).strip()

def summarize_articles(articles):
    full_text = ""
    for article in articles:
        title = article['title']
        summary = article['summary']
        full_text += f"{title}. {summary} "

    full_text = clean_text(full_text)
    
    # BART funciona mejor con textos de 500-1024 tokens
    if len(full_text) > 1024:
        full_text = full_text[:1024]

    try:
        result = summarizer(full_text, max_length=150, min_length=60, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        print("Error en resumen:", str(e))
        return "No se pudo generar el resumen automáticamente."
