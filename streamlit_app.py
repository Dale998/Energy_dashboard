import json
import os
from datetime import datetime
from html.parser import HTMLParser

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

# Importa la funzione di refresh da fetch_data
try:
    from fetch_data import refresh_sources as fetch_data_refresh_sources
except ImportError:
    fetch_data_refresh_sources = None

DATA_DIR = "data"
TEMATICHE_MAP = {
    "Idrogeno": "hydrogen.json",
    "Nucleare": "nuclear.json",
    "Data Center": "datacenter.json",
    "Biocarburanti e Biogas": "biocarburanti_biogas.json",
    "Geotermico": "geotermico.json",
    "Cogenerazione": "cogenerazione.json"
}

st.set_page_config(page_title="Dashboard Energia", layout="wide")
st.title("🔋 Dashboard Tematiche Energetiche")

def load_tematica_data(tematica):
    """Carica i dati per una tematica specifica"""
    filename = TEMATICHE_MAP.get(tematica)
    if not filename:
        return {}
    
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return {}
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Errore nel caricamento dati: {e}")
        return {}

def safe_float(value):
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None

def format_link(url):
    return f"[Fonte]({url})" if url else ""

def render_metric_card(label, value, emoji, key, color="#2b6cb0"):
    card_html = f"""
    <div style="
        background: linear-gradient(135deg, {color} 0%, #1a365d 100%);
        border-radius: 20px;
        padding: 24px;
        color: white;
        text-align: center;
        box-shadow: 0 16px 30px rgba(0, 0, 0, 0.18);
        min-height: 170px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    ">
      <div style="font-size: 24px; font-weight: 700; margin-bottom: 12px;">{emoji} {label}</div>
      <div style="font-size: 56px; font-weight: 900; letter-spacing: 0.02em;">{value}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
    return st.button(f"Mostra {label}", key=key)

# UI principale
TEMATICHE = list(TEMATICHE_MAP.keys())

st.sidebar.header("🎯 Seleziona Tematica")
tematica = st.sidebar.selectbox("Tematica energetica", TEMATICHE, index=0)

# Carica dati per la tematica selezionata
tematica_data = load_tematica_data(tematica)

if not tematica_data:
    st.error(f"Impossibile caricare i dati per {tematica}")
    st.stop()

st.sidebar.header("📥 Inserisci nuovi dati")
with st.sidebar.expander("➕ Aggiungi progetto"):
    st.info("Usa il template in templates/project_template.json")

with st.sidebar.expander("➕ Aggiungi normativa"):
    st.info("Usa il template in templates/normativa_template.json")

if st.sidebar.button("🔄 Aggiorna fonti ufficiali"):
    if fetch_data_refresh_sources:
        fetch_data_refresh_sources({}, {}, tematica)
        st.sidebar.success("✅ Fonti aggiornate!")
        tematica_data = load_tematica_data(tematica)

st.sidebar.markdown("---")
st.sidebar.markdown("**Nota:** I dati vengono caricati da file JSON strutturati nella cartella `/data`")

# Display principale
st.header(f"📊 {tematica_data.get('tematica', tematica)}")

progetti_italia = len(tematica_data.get('progetti', {}).get('italia', []))
progetti_europa = len(tematica_data.get('progetti', {}).get('europa', []))
progetti_mondo = len(tematica_data.get('progetti', {}).get('mondo', []))

# Metriche
col1, col2, col3 = st.columns(3)

with col1:
    if render_metric_card("Progetti Italia", progetti_italia, "🇮🇹", "btn_italy", color="#1f77b4"):
        st.session_state["show_italy"] = not st.session_state.get("show_italy", False)

with col2:
    if render_metric_card("Progetti Europa", progetti_europa, "🇪🇺", "btn_europe", color="#2ca02c"):
        st.session_state["show_europe"] = not st.session_state.get("show_europe", False)

with col3:
    if render_metric_card("Progetti Mondo", progetti_mondo, "🌍", "btn_world", color="#ff7f0e"):
        st.session_state["show_world"] = not st.session_state.get("show_world", False)

st.markdown("---")

# Mostra tabelle progetti
if st.session_state.get("show_italy"):
    st.subheader("🇮🇹 Progetti in Italia")
    progetti_it = tematica_data.get('progetti', {}).get('italia', [])
    if progetti_it:
        df = pd.DataFrame(progetti_it)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nessun progetto in Italia")

if st.session_state.get("show_europe"):
    st.subheader("🇪🇺 Progetti in Europa")
    progetti_eu = tematica_data.get('progetti', {}).get('europa', [])
    if progetti_eu:
        df = pd.DataFrame(progetti_eu)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nessun progetto in Europa")

if st.session_state.get("show_world"):
    st.subheader("🌍 Progetti nel Mondo")
    progetti_w = tematica_data.get('progetti', {}).get('mondo', [])
    if progetti_w:
        df = pd.DataFrame(progetti_w)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("Nessun progetto mondiale")

# Mappa
st.subheader("🗺️ Mappa progetti")
all_progetti = (
    tematica_data.get('progetti', {}).get('italia', []) +
    tematica_data.get('progetti', {}).get('europa', []) +
    tematica_data.get('progetti', {}).get('mondo', [])
)

valid_progetti = [p for p in all_progetti if safe_float(p.get("lat")) and safe_float(p.get("lon"))]

if valid_progetti:
    m = folium.Map(location=[50, 10], zoom_start=4)
    for prog in valid_progetti:
        folium.Marker(
            location=[prog["lat"], prog["lon"]],
            popup=f"<b>{prog.get('nome')}</b><br>{prog.get('descrizione')}<br>Capacità: {prog.get('capacita_mw')} MW",
            tooltip=prog.get("nome"),
        ).add_to(m)
    st_folium(m, width=700, height=500)
else:
    st.info("Nessuna posizione valida per i progetti")

# Normative
st.subheader("📜 Normativa vigente")

normative_it = tematica_data.get('normative', {}).get('italia', [])
normative_eu = tematica_data.get('normative', {}).get('europa', [])

col_norm1, col_norm2 = st.columns(2)

with col_norm1:
    st.markdown("**🇮🇹 Normative Italiane**")
    if normative_it:
        for norm in normative_it:
            with st.expander(f"📋 {norm.get('titolo', 'N/A')[:50]}..."):
                st.write(f"**Tipo:** {norm.get('tipo')}")
                st.write(f"**Anno:** {norm.get('anno')}")
                st.write(f"**Descrizione:** {norm.get('descrizione')}")
                
                if norm.get('punti_principali'):
                    st.write("**Punti principali:**")
                    for punto in norm.get('punti_principali', []):
                        st.write(f"• {punto}")
                
                if norm.get('url'):
                    st.markdown(f"[🔗 Leggi il testo completo]({norm.get('url')})")
    else:
        st.info("Nessuna normativa italiana disponibile")

with col_norm2:
    st.markdown("**🇪🇺 Normative Europee**")
    if normative_eu:
        for norm in normative_eu:
            with st.expander(f"📋 {norm.get('titolo', 'N/A')[:50]}..."):
                st.write(f"**Tipo:** {norm.get('tipo')}")
                st.write(f"**Anno:** {norm.get('anno')}")
                st.write(f"**Descrizione:** {norm.get('descrizione')}")
                
                if norm.get('punti_principali'):
                    st.write("**Punti principali:**")
                    for punto in norm.get('punti_principali', []):
                        st.write(f"• {punto}")
                
                if norm.get('url'):
                    st.markdown(f"[🔗 Leggi il testo completo]({norm.get('url')})")
    else:
        st.info("Nessuna normativa europea disponibile")

# Fonti ufficiali
st.subheader("🔗 Fonti ufficiali")
fonti = tematica_data.get('fonti_ufficiali', [])
if fonti:
    cols = st.columns(min(3, len(fonti)))
    for idx, fonte in enumerate(fonti):
        with cols[idx % len(cols)]:
            with st.container(border=True):
                st.write(f"**{fonte.get('nome')}**")
                st.caption(fonte.get('tipo', ''))
                st.write(fonte.get('descrizione', ''))
                if fonte.get('url'):
                    st.markdown(f"[🌐 Visita il sito]({fonte.get('url')})")

st.divider()
st.caption(f"Dashboard aggiornata: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")