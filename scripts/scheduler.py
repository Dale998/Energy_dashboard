"""
Scheduler per aggiornamenti automatici periodici
Esegue gli aggiornamenti ogni X ore/giorni con threading
"""

import schedule
import time
import logging
import threading
from auto_updater import EnergyDataUpdater
from datetime import datetime
import sys
import os

# Aggiungi il parent directory al path per importare auto_updater
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UpdateScheduler:
    """Gestisce gli aggiornamenti programmati con threading"""
    
    def __init__(self):
        self.updater = EnergyDataUpdater()
        self.running = False
        self.scheduler_thread = None
        os.makedirs('logs', exist_ok=True)
    
    def run_in_thread(self, job_func, job_name):
        """Esegue un job in un thread separato"""
        def thread_wrapper():
            try:
                logger.info(f"🔄 Inizio: {job_name}")
                job_func()
                logger.info(f"✅ Completato: {job_name}")
            except Exception as e:
                logger.error(f"❌ Errore in {job_name}: {e}", exc_info=True)
        
        thread = threading.Thread(target=thread_wrapper, name=job_name, daemon=True)
        thread.start()
    
    def job_complete_update(self):
        """Job: Aggiornamento completo"""
        self.run_in_thread(
            self.updater.run_all_updates,
            "Aggiornamento Completo"
        )
    
    def job_regulations(self):
        """Job: Aggiornamento normative"""
        self.run_in_thread(
            self.updater.update_regulations,
            "Aggiornamento Normative"
        )
    
    def job_hydrogen(self):
        """Job: Aggiornamento idrogeno"""
        self.run_in_thread(
            self.updater.update_hydrogen,
            "Aggiornamento Idrogeno"
        )
    
    def job_biogas(self):
        """Job: Aggiornamento biogas"""
        self.run_in_thread(
            self.updater.update_biogas_biocarburanti,
            "Aggiornamento Biogas"
        )
    
    def job_nuclear(self):
        """Job: Aggiornamento nucleare"""
        self.run_in_thread(
            self.updater.update_nuclear,
            "Aggiornamento Nucleare"
        )
    
    def job_datacenters(self):
        """Job: Aggiornamento data center"""
        self.run_in_thread(
            self.updater.update_datacenters,
            "Aggiornamento Data Center"
        )
    
    def job_geothermal(self):
        """Job: Aggiornamento geotermico"""
        self.run_in_thread(
            self.updater.update_geothermal,
            "Aggiornamento Geotermico"
        )
    
    def job_cogeneration(self):
        """Job: Aggiornamento cogenerazione"""
        self.run_in_thread(
            self.updater.update_cogeneration,
            "Aggiornamento Cogenerazione"
        )
    
    def schedule_updates(self):
        """Configura gli aggiornamenti programmati"""
        
        # Cancella jobs precedenti
        schedule.clear()
        
        # Aggiornamento completo ogni 6 ore
        schedule.every(6).hours.do(self.job_complete_update).tag('complete')
        
        # Aggiornamento normative ogni 24 ore alle 02:00
        schedule.every().day.at("02:00").do(self.job_regulations).tag('regulations')
        
        # Aggiornamento hydrogen ogni 4 ore
        schedule.every(4).hours.do(self.job_hydrogen).tag('hydrogen')
        
        # Aggiornamento biogas ogni 12 ore
        schedule.every(12).hours.do(self.job_biogas).tag('biogas')
        
        # Aggiornamento nucleare ogni 24 ore
        schedule.every(24).hours.do(self.job_nuclear).tag('nuclear')
        
        # Aggiornamento data center ogni 12 ore
        schedule.every(12).hours.do(self.job_datacenters).tag('datacenters')
        
        # Aggiornamento geotermico ogni 24 ore
        schedule.every(24).hours.do(self.job_geothermal).tag('geothermal')
        
        # Aggiornamento cogenerazione ogni 24 ore
        schedule.every(24).hours.do(self.job_cogeneration).tag('cogeneration')
        
        logger.info("✅ Scheduler configurato con i seguenti job:")
        for job in schedule.jobs:
            logger.info(f"  • {job.tag}: ogni {job.interval} {job.unit}")
    
    def _run_scheduler(self):
        """Loop interno dello scheduler (in thread)"""
        logger.info("🚀 Scheduler loop avviato")
        
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(60)  # Verifica ogni minuto
        except Exception as e:
            logger.error(f"❌ Errore nel scheduler loop: {e}", exc_info=True)
        finally:
            logger.info("⛔ Scheduler loop fermato")
    
    def start(self):
        """Avvia lo scheduler in un thread separato"""
        if self.running:
            logger.warning("⚠️ Scheduler è già in esecuzione")
            return
        
        self.schedule_updates()
        self.running = True
        
        # Avvia il loop dello scheduler in un thread daemon
        self.scheduler_thread = threading.Thread(
            target=self._run_scheduler,
            name="SchedulerThread",
            daemon=True
        )
        self.scheduler_thread.start()
        
        logger.info("✅ Scheduler avviato in background")
        
        # Esegui un aggiornamento iniziale
        logger.info("📋 Esecuzione aggiornamento iniziale...")
        self.job_complete_update()
    
    def stop(self):
        """Ferma lo scheduler"""
        if not self.running:
            logger.warning("⚠️ Scheduler non è in esecuzione")
            return
        
        self.running = False
        logger.info("🛑 Scheduler fermato")
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)


def main():
    """Funzione principale"""
    scheduler = UpdateScheduler()
    
    try:
        scheduler.start()
        
        # Mantieni il programma in esecuzione
        logger.info("⏳ Scheduler in esecuzione. Premi Ctrl+C per fermare...")
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        logger.info("\n⛔ Interruzione utente")
        scheduler.stop()
    
    except Exception as e:
        logger.error(f"❌ Errore critico: {e}", exc_info=True)
        scheduler.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()