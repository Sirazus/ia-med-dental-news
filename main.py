# main.py
from scraper import get_news
from summarizer import summarize_articles
from email_sender import send_email
import os

def main():
    print("🔍 Buscando noticias...")
    articles = get_news()
    
    if not articles:
        print("No se encontraron artículos.")
        return
    
    print(f"✅ {len(articles)} artículos encontrados. Resumiendo...")
    summary = summarize_articles(articles)
    
    # Guardar resumen para Notebook LM
    if not os.path.exists("output"):
        os.makedirs("output")
    with open("output/podcast_script.txt", "w", encoding="utf-8") as f:
        f.write(summary)
    
    print("📧 Enviando email con el resumen...")
    send_email(summary)

if __name__ == "__main__":
    main()
