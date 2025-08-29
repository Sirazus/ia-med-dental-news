# main.py
from scraper import get_news
from summarizer import summarize_articles
import os
from datetime import datetime

def main():
    print("🚀 Iniciando generación del resumen semanal...\n")

    # Crear carpeta output si no existe
    if not os.path.exists("output"):
        os.makedirs("output")
        print("📁 Carpeta 'output' creada.\n")

    # 1. Obtener noticias
    print("🔍 Buscando noticias sobre IA en medicina y odontología...\n")
    articles = get_news()

    if not articles:
        print("❌ No se encontraron artículos esta semana.")
        return

    print(f"✅ {len(articles)} artículos encontrados:\n")
    for i, article in enumerate(articles):
        print(f"{i+1}. {article['title']}")

    # 2. Resumir con IA
    print("\n📝 Generando resumen con IA...")
    summary = summarize_articles(articles)
    print(f"\n✨ Resumen generado:\n{summary}\n")

    # 3. Guardar en archivo con fecha
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"output/resumen-semanal-{date_str}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"📅 Resumen Semanal: IA en Medicina y Odontología\n")
        f.write(f"📆 Fecha: {date_str}\n")
        f.write(f"🔗 Fuente: Google News, PubMed\n\n")
        f.write(f"📰 Noticias destacadas:\n\n")
        for i, article in enumerate(articles):
            f.write(f"{i+1}. {article['title']}\n")
            f.write(f"   🔗 {article['link']}\n\n")
        f.write(f"📝 Resumen:\n\n{summary}\n")
        f.write(f"\n🎙️ Próximo paso: Copia este texto y pásalo a Notebook LM para generar el podcast.\n")

    print(f"✅ Resumen guardado en: {filename}")

if __name__ == "__main__":
    main()
