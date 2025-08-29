# main.py
from scraper import get_news
from summarizer import summarize_articles
import os

def main():
    print("🔍 Buscando noticias...")
    articles = get_news()
    
    if not articles:
        print("No se encontraron artículos.")
        return
    
    print(f"✅ {len(articles)} artículos encontrados. Resumiendo...")
    summary = summarize_articles(articles)
    
    # Crear carpeta output si no existe
    if not os.path.exists("output"):
        os.makedirs("output")
    
    # Guardar resumen en un archivo con fecha
    from datetime import datetime
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"output/resumen-semanal-{date_str}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📅 Resumen semanal: IA en Medicina y Odontología\n")
        f.write(f"📆 Fecha: {date_str}\n\n")
        f.write(f"📰 Noticias destacadas:\n\n")
        f.write(summary)
    
    print(f"✅ Resumen guardado en {filename}")

if __name__ == "__main__":
    main()
