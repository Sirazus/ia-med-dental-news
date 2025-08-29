# scraper.py
import feedparser
import requests
from bs4 import BeautifulSoup
import re
import time
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔑 Palabras clave relevantes para IA en medicina y odontología
KEYWORDS = {
    'ia', 'inteligencia artificial', 'machine learning', 'deep learning', 'neural network',
    'medicina', 'odontología', 'dental', 'salud', 'diagnóstico', 'radiología',
    'ai', 'healthcare', 'medical', 'dentistry', 'clinical', 'prediction', 'algorithm'
}

# 🚫 Dominios no deseados (fuentes generales o irrelevantes)
BLACKLISTED_DOMAINS = {
    'radionacional.co',
    'elnuevodia.com',
    'lavanguardia.com',
    'eltiempo.com',  # opcional: quitar si hay noticias buenas
    'semana.com',
    'wikipedia.org'
}

# 🌐 Fuentes confiables y especializadas
RSS_FEEDS = [
    "https://pubmed.ncbi.nlm.nih.gov/rss/search/1IiVQZ5a5VZ5Zx-ai9aQ5aQ5aQ5aQ5aQ5a/?format=rss",  # PubMed: IA en medicina
    "https://arxiv.org/rss/cs.AI",  # arXiv: IA (filtraremos después)
    "https://www.nature.com/subjects/artificial-intelligence/rss",  # Nature
    "https://www.dentistrytoday.com/feed/"  # Dentistry Today
]

def clean_text(text):
    """Limpia y normaliza el texto"""
    if not text:
        return ""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\.{2,}', '', text)  # Elimina puntos extraños
    return text.strip()

def is_relevant(title, content=""):
    """
    Determina si un artículo es relevante: IA + (medicina o odontología)
    Más inclusivo, menos estricto
    """
    text = f"{title} {content}".lower()

    # Palabras clave de IA (más amplias)
    ai_keywords = {
        'ia', 'inteligencia artificial', 'machine learning', 'deep learning',
        'neural network', 'red neuronal', 'algoritmo', 'llm', 'generative ai',
        'ai', 'artificial intelligence', 'automated', 'predictivo', 'modelo',
        'intelligent system', 'decision support', 'automated diagnosis'
    }

    # Medicina y salud
    medical_keywords = {
        'medicina', 'salud', 'clínico', 'diagnóstico', 'enfermedad',
        'hospital', 'médico', 'doctor', 'tratamiento', 'medical',
        'healthcare', 'clinical', 'disease', 'radiología', 'oncología',
        'neurología', 'patología', 'precision medicine', 'digital health'
    }

    # Odontología y dental
    dental_keywords = {
        'odontología', 'dental', 'dentista', 'caries', 'implante',
        'ortodoncia', 'prótesis', 'periodontal', 'endodoncia',
        'dental implant', 'tooth decay', 'prosthodontics', 'orthodontics',
        'oral health', 'dental imaging', 'dental AI', 'dentistry'
    }

    has_ai = any(kw in text for kw in ai_keywords)
    has_medical = any(kw in text for kw in medical_keywords)
    has_dental = any(kw in text for kw in dental_keywords)

    return has_ai and (has_medical or has_dental)
def is_blacklisted(url):
    """Verifica si el dominio está en la lista negra"""
    return any(domain in url.lower() for domain in BLACKLISTED_DOMAINS)

def extract_from_pubmed_abstract(entry):
    """Extrae resumen de PubMed cuando no se puede scrapear"""
    summary = entry.get('summary', '')
    # Limpiar HTML
    summary = re.sub(r'<[^>]+>', '', summary)
    return clean_text(summary)

def extract_from_dentistrytoday(soup):
    """Estrategia específica para Dentistry Today"""
    content = soup.find('div', class_='entry-content')
    if content:
        for el in content(['script', 'style', 'img', 'aside', 'figure']):
            el.decompose()
        return clean_text(content.get_text()[:2000])
    return ""

def extract_from_nature(soup):
    """Estrategia para Nature"""
    content = soup.find('div', class_='c-article-body')
    if content:
        return clean_text(content.get_text()[:2000])
    return ""

def extract_from_arxiv(soup):
    """Estrategia para arXiv"""
    content = soup.find('div', class_='abstract')
    if content:
        return clean_text(content.get_text().replace('Abstract:', ''))
    return ""

def extract_general_content(soup):
    """Extracción genérica para otros sitios"""
    selectors = [
        'article',
        '.article-body', '.post-content', '.content', '.entry-content',
        '[role="main"]', 'main', '.story', '.article__body'
    ]
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            text = " ".join([clean_text(el.get_text()) for el in elements])
            if len(text) > 200:
                return text[:2000]
    # Fallback: cuerpo completo
    body = soup.find('body')
    if body:
        return clean_text(body.get_text())[:2000]
    return ""

def extract_text_from_url(url, title=""):
    """Extrae el contenido principal de una URL con estrategias por dominio"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    
    # Estrategias por dominio
    if 'pubmed.ncbi.nlm.nih.gov' in url:
        return "Artículo científico disponible en el enlace. Consulta el resumen en PubMed."  # Ya viene en el RSS
    elif 'arxiv.org' in url:
        pass  # Se procesa después
    elif 'nature.com' in url:
        pass  # Se procesa después
    elif 'dentistrytoday.com' in url:
        pass  # Se procesa después

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Aplicar estrategia por dominio
        if 'dentistrytoday.com' in url:
            return extract_from_dentistrytoday(soup)
        elif 'nature.com' in url:
            return extract_from_nature(soup)
        elif 'arxiv.org' in url:
            return extract_from_arxiv(soup)
        else:
            return extract_general_content(soup)

    except Exception as e:
        logger.warning(f"⚠️  No se pudo extraer {url}: {str(e)}")
        return "No se pudo extraer el contenido. Revisa el enlace."

def get_news():
    """Obtiene noticias relevantes de fuentes especializadas"""
    articles = []
    seen_titles = set()

    for feed_url in RSS_FEEDS:
        logger.info(f"🔍 Buscando en fuente: {feed_url}")
        try:
            feed = feedparser.parse(feed_url)
            if not feed.entries:
                logger.warning(f"⚠️  No se encontraron entradas en {feed_url}")
                continue

            for entry in feed.entries[:10]:  # Máximo 10 por fuente
                title = entry.get('title', 'Sin título').strip()
                link = entry.get('link', '').strip()
                if not title or not link:
                    continue

                # Normalizar título para evitar duplicados
                norm_title = title.lower()
                if norm_title in seen_titles:
                    continue
                seen_titles.add(norm_title)

                # Verificar si está en lista negra
                if is_blacklisted(link):
                    logger.info(f"🚫 Saltado (blacklist): {link}")
                    continue

                # Verificar relevancia por título
                if not is_relevant(title):
                    logger.info(f"❌ Irrelevante (título): {title}")
                    continue

                logger.info(f"📄 Procesando: {title}")

                # Extraer contenido
                if 'pubmed.ncbi.nlm.nih.gov' in link:
                    content = extract_from_pubmed_abstract(entry)
                else:
                    content = extract_text_from_url(link, title)
                    time.sleep(1.5)  # Etiqueta de respeto (1.5s entre requests)

                # Verificar relevancia del contenido
                if not is_relevant(title, content):
                    logger.info(f"❌ Irrelevante (contenido): {title}")
                    continue

                articles.append({
                    'title': title,
                    'link': link,
                    'content': content,
                    'source': entry.get('source', {}).get('title', 'Desconocida'),
                    'published': entry.get('published', 'Fecha desconocida')
                })

                if len(articles) >= 8:  # Máximo 8 artículos
                    break
            if len(articles) >= 8:
                break
        except Exception as e:
            logger.error(f"❌ Error procesando feed {feed_url}: {str(e)}")

    logger.info(f"✅ {len(articles)} artículos relevantes encontrados.")
    return articles
