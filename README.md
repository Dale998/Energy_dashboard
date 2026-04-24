# 🔋 Dashboard Tematiche Energetiche

Una dashboard interattiva Streamlit per monitorare progetti e normative nelle principali tematiche energetiche: Idrogeno, Nucleare, Data Center, Biocarburanti e Biogas, Geotermico, Cogenerazione.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://energy-dashboard.streamlit.app/)

## 📊 Funzionalità

### Dashboard Interattiva
- **Metriche principali**: Numero progetti per Italia, Europa e Mondo
- **Progetti attivi**: Tabella dettagliata con capacità, stato, costi e ubicazioni
- **Mappa geografica**: Visualizzazione progetti su mappa interattiva
- **Grafici storici**: Evoluzione temporale dei progetti
- **Normativa**: Elenco completo delle normative vigenti
- **Selettore normativo**: Sommari dettagliati delle normative selezionate

### Tematiche Energetiche
1. **🟢 Idrogeno**: Progetti idrogeno verde, elettrolisi, filiere
2. **⚛️ Nucleare**: Reattori nucleari, sicurezza, cooperazione internazionale
3. **💻 Data Center**: Efficienza energetica, raffreddamento sostenibile
4. **🌱 Biocarburanti e Biogas**: Biometano, digestione anaerobica, biocarburanti avanzati
5. **🌋 Geotermico**: Energia geotermica, pompe di calore, campi geotermici
6. **🔄 Cogenerazione**: Produzione combinata calore-elettricità, efficienza energetica

## 🚀 Installazione e Avvio

### Prerequisiti
- Python 3.8+
- PostgreSQL (opzionale, per dati persistenti)

### Installazione
1. Clona il repository:
   ```bash
   git clone https://github.com/your-repo/energy-dashboard.git
   cd energy-dashboard
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura le API keys in `config.json`:
   ```json
   {
     "api_keys": {
       "eur_lex": "your_eur_lex_api_key",
       "iaea": "your_iaea_api_key",
       "irena": "your_irena_api_key",
       "gse": "your_gse_api_key"
     }
   }
   ```

4. (Opzionale) Configura il database PostgreSQL:
   ```sql
   -- Esegui schema.sql per creare le tabelle
   psql -d energy_dashboard -f schema.sql
   ```

### Avvio
```bash
streamlit run streamlit_app.py
```

L'applicazione sarà disponibile su `http://localhost:8501`

## 📁 Struttura del Progetto

```
energy-dashboard/
├── streamlit_app.py      # Applicazione principale Streamlit
├── fetch_data.py         # Script per aggiornamento automatico fonti
├── update_data.py        # CLI per inserimento dati
├── schema.sql           # Schema database PostgreSQL
├── config.json          # Configurazioni API e database
├── data_store.json      # Archivio centralizzato dati
├── requirements.txt     # Dipendenze Python
└── README.md           # Questa documentazione
```

## 🔧 Configurazione

### API Keys
Il file `config.json` contiene le configurazioni per le fonti dati:
- **EUR-Lex**: Database legislativo europeo
- **IAEA**: Agenzia Internazionale per l'Energia Atomica
- **IRENA**: Agenzia Internazionale per le Energie Rinnovabili
- **GSE**: Gestore Servizi Energetici (Italia)
- **ENTSOG**: Rete Europea dei Gestori di Sistemi di Trasporto Gas
- **Clean Hydrogen Partnership**: Iniziativa europea per l'idrogeno pulito

### Database
Configurazione PostgreSQL per dati persistenti:
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "database": "energy_dashboard",
    "user": "energy_user",
    "password": "your_password"
  }
}
```

## 📊 Fonti Dati

### Progetti
- **Idrogeno**: Clean Hydrogen Partnership, ENTSOG, GSE
- **Nucleare**: IAEA PRIS, EURATOM
- **Data Center**: Codice di Condotta UE, Direttiva Efficienza Energetica
- **Biocarburanti/Biogas**: EBA, Direttiva Rifiuti UE
- **Geotermico**: IRENA, GSE, Direttiva Energie Rinnovabili
- **Cogenerazione**: Direttiva Efficienza Energetica, GSE

### Normativa
- **EUR-Lex**: Database legislativo europeo
- **Normattiva.it**: Leggi italiane
- **Direttive UE**: RED III, EED, Waste Framework Directive

## 🔄 Aggiornamento Dati

### Aggiornamento automatico delle fonti
```bash
# Aggiorna tutte le fonti ufficiali (da config.json) e personalizzate
python fetch_data.py refresh-sources
```

Questo comando:
- legge le URL ufficiali da `config.json`
- legge le fonti personalizzate da `data_store.json`
- estrae i metadati (titolo, descrizione) da ogni URL
- aggiorna `data_store.json` con i metadati e il timestamp `last_checked`

### Inserimento progetti e normative (CLI)

- Per aggiungere un progetto completo:
  ```bash
  python update_data.py add-project --tematica "Idrogeno" --nome "Nome Progetto" --paese "Italia" --capacita_mw 20 --stato "attivo" --descrizione "..." --costo 10 --luogo "Milano" --lat 45.46 --lon 9.19 --url "https://..."
  ```

- Per aggiungere un progetto basato su un link:
  ```bash
  python update_data.py add-project-url --tematica "Idrogeno" --url "https://..." --paese "Italia"
  ```

- Per aggiungere una normativa:
  ```bash
  python update_data.py add-normativa --tematica "Idrogeno" --titolo "Proposta UE" --tipo "Comunicazione" --anno 2025 --url "https://..." --sommario "..."
  ```

- Per aggiungere una fonte personalizzata:
  ```bash
  python update_data.py add-source --tematica "Idrogeno" --url "https://example.com/fonte" --label "EUR-Lex progetto idrogeno"
  ```

### Inserimento diretto dall'app
Apri l'app Streamlit (`streamlit run streamlit_app.py`) e usa il pannello laterale per:
- Selezionare la tematica
- Aggiungere un progetto o una normativa
- Aggiungere una fonte personalizzata per la tematica selezionata
- Premere **"Aggiorna fonti ufficiali e aggiunte"** per aggiornare i metadati di tutte le fonti

### Struttura dati (data_store.json)
```json
{
  "projects": {
    "Idrogeno": [{...}],
    "Nucleare": [{...}]
  },
  "normative": {
    "Idrogeno": [{...}],
    "Nucleare": [{...}]
  },
  "statistics": {
    "Idrogeno": {...}
  },
  "sources": {
    "Idrogeno": [
      {
        "url": "https://...",
        "label": "EUR-Lex",
        "type": "official",
        "title": "...",
        "description": "...",
        "last_checked": "2026-04-24T12:30:20..."
      }
    ]
  }
}
```

## 🛠️ Tecnologie Utilizzate

- **Streamlit**: Framework web per dashboard interattive
- **Pandas**: Manipolazione e analisi dati
- **Plotly**: Grafici interattivi
- **Folium**: Mappe geografiche
- **BeautifulSoup4**: Web scraping per estrazione metadati
- **Requests**: Chiamate HTTP per API
- **PostgreSQL**: Database relazionale (opzionale)

## 📈 Metriche Disponibili

- Numero progetti attivi per paese/area geografica
- Capacità installata (MW)
- Costi di investimento (milioni €)
- Stato progetti (attivo, in costruzione, pianificato)
- Evoluzione storica progetti
- Link a fonti ufficiali e personalizzate

## 🎯 Roadmap

- [ ] Integrazione database PostgreSQL completa
- [ ] API REST per accesso dati esterni
- [ ] Dashboard mobile responsive
- [ ] Notifiche aggiornamenti automatici
- [ ] Esportazione dati in CSV/Excel
- [ ] Filtri avanzati e ricerca
- [ ] Dashboard comparativa tra tematiche
- [ ] Scheduler automatico per aggiornamenti periodici

## 🤝 Contributi

Contributi benvenuti! Per modifiche significative:
1. Apri una issue per discutere la proposta
2. Crea un branch feature
3. Invia una pull request

## 📄 Licenza

Questo progetto è distribuito sotto licenza MIT. Vedi il file `LICENSE` per dettagli.
