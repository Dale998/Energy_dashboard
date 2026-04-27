-- Tematiche energetiche
CREATE TABLE tematiche (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,  -- 'idrogeno', 'nucleare', 'biogas'...
    descrizione TEXT
);

-- Progetti
CREATE TABLE progetti (
    id SERIAL PRIMARY KEY,
    tematica_id INT REFERENCES tematiche(id),
    nome VARCHAR(255),
    paese VARCHAR(100),
    regione VARCHAR(100),  -- 'Italia', 'Europa', 'Mondo'
    stato VARCHAR(50),     -- 'attivo', 'completato', 'pianificato'
    capacita_mw DECIMAL,
    data_inizio DATE,
    data_fine DATE,
    fonte_url TEXT,
    aggiornato_il TIMESTAMP DEFAULT NOW()
);

-- Normativa
CREATE TABLE normativa (
    id SERIAL PRIMARY KEY,
    tematica_id INT REFERENCES tematiche(id),
    titolo VARCHAR(500),
    tipo VARCHAR(50),      -- 'direttiva UE', 'decreto', 'regolamento'
    ambito VARCHAR(50),    -- 'Italia', 'UE', 'internazionale'
    data_pubblicazione DATE,
    url TEXT,
    sintesi TEXT
);

-- Serie storiche (per grafici)
CREATE TABLE storico_progetti (
    id SERIAL PRIMARY KEY,
    tematica_id INT REFERENCES tematiche(id),
    anno INT,
    regione VARCHAR(100),
    num_progetti INT,
    capacita_totale_mw DECIMAL
);