"""
Script per aggiornare automaticamente i dati della dashboard energetica
dalle fonti ufficiali specificate e dalle fonti personalizzate.
"""

import requests
import json
import pandas as pd
from datetime import datetime
import time
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEMATICHE = ["Idrogeno", "Nucleare", "Data Center", "Biocarburanti e Biogas", "Geotermico", "Cogenerazione"]
DATA_DIR = "data"

def load_json(filepath):
    """Carica un file JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_json(filepath, data):
    """Salva dati in JSON"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def fetch_metadata_from_url(url):
    """
    Estrae il titolo e la descrizione da un URL
    Ritorna: {"title": "...", "description": "..."}
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=10, headers=headers)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Estrai il titolo
        title = None
        if soup.find('title'):
            title = soup.find('title').string
        elif soup.find('h1'):
            title = soup.find('h1').string
        else:
            title = url.split('/')[-1][:50]
        
        # Estrai la descrizione
        description = ""
        og_description = soup.find('meta', {'property': 'og:description'})
        if og_description:
            description = og_description.get('content', '')
        else:
            meta_description = soup.find('meta', {'name': 'description'})
            if meta_description:
                description = meta_description.get('content', '')
        
        return {
            "title": title[:100] if title else "No title",
            "description": description[:200] if description else "No description",
            "last_checked": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.warning(f"Errore nel fetch metadati da {url}: {e}")
        return {
            "title": "Fetch error",
            "description": str(e)[:100],
            "last_checked": datetime.now().isoformat()
        }

def refresh_sources_for_tematica(tematica_file):
    """
    Aggiorna le fonti ufficiali per una tematica specifica
    """
    data = load_json(tematica_file)
    
    if 'fonti_ufficiali' not in data:
        return data
    
    logger.info(f"🔄 Aggiornamento fonti per {data.get('tematica', 'Unknown')}...")
    
    for fonte in data['fonti_ufficiali']:
        if 'url' in fonte and fonte['url'].startswith('http'):
            metadata = fetch_metadata_from_url(fonte['url'])
            fonte.update(metadata)
            logger.info(f"✅ Aggiornato: {metadata['title']}")
            time.sleep(0.5)  # Evita throttling
    
    return data

def refresh_all_sources():
    """
    Aggiorna tutte le fonti per tutte le tematiche
    """
    logger.info("🔄 Inizio aggiornamento tutte le fonti...")
    
    if not os.path.exists(DATA_DIR):
        logger.error(f"Directory {DATA_DIR} non trovata!")
        return
    
    # Mappa tra nome tematica e file JSON
    tematica_files = {
        "Idrogeno": f"{DATA_DIR}/hydrogen.json",
        "Nucleare": f"{DATA_DIR}/nuclear.json",
        "Data Center": f"{DATA_DIR}/datacenter.json",
        "Biocarburanti e Biogas": f"{DATA_DIR}/biocarburanti_biogas.json",
        "Geotermico": f"{DATA_DIR}/geotermico.json",
        "Cogenerazione": f"{DATA_DIR}/cogenerazione.json"
    }
    
    for tematica, filepath in tematica_files.items():
        if os.path.exists(filepath):
            updated_data = refresh_sources_for_tematica(filepath)
            save_json(filepath, updated_data)
            logger.info(f"✅ Salvato: {filepath}")
        else:
            logger.warning(f"⚠️ File non trovato: {filepath}")
    
    logger.info("✅ Aggiornamento fonti completato!")

def refresh_sources(data, config, tematica):
    """
    Wrapper per compatibilità con streamlit_app.py
    Aggiorna le fonti per una tematica specifica
    """
    tematica_files = {
        "Idrogeno": f"{DATA_DIR}/hydrogen.json",
        "Nucleare": f"{DATA_DIR}/nuclear.json",
        "Data Center": f"{DATA_DIR}/datacenter.json",
        "Biocarburanti e Biogas": f"{DATA_DIR}/biocarburanti_biogas.json",
        "Geotermico": f"{DATA_DIR}/geotermico.json",
        "Cogenerazione": f"{DATA_DIR}/cogenerazione.json"
    }
    
    if tematica in tematica_files:
        filepath = tematica_files[tematica]
        if os.path.exists(filepath):
            updated_data = refresh_sources_for_tematica(filepath)
            save_json(filepath, updated_data)
            logger.info(f"✅ Fonti aggiornate per {tematica}")

if __name__ == "__main__":
    refresh_all_sources()
    print("\n💡 Per aggiornamenti automatici, considerare:")
    print("   1. APScheduler per aggiornamenti periodici")
    print("   2. API dirette da fonti ufficiali")
    print("   3. Scraping strutturato con validazione dati")
    print("   4. Backup automatici giornalieri")