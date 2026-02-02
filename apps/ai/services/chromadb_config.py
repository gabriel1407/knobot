"""
Configuración para silenciar warnings de ChromaDB.
"""
import warnings
import logging

# Silenciar warnings específicos de ChromaDB telemetry
warnings.filterwarnings('ignore', message='.*telemetry.*')
warnings.filterwarnings('ignore', message='.*capture.*')

# Configurar logging de ChromaDB para solo mostrar errores críticos
logging.getLogger('chromadb').setLevel(logging.ERROR)
logging.getLogger('chromadb.telemetry').setLevel(logging.CRITICAL)

# Silenciar warnings de IDs duplicados
class ChromaDBWarningFilter(logging.Filter):
    """Filtro para silenciar warnings específicos de ChromaDB."""
    
    def filter(self, record):
        # Silenciar warnings de telemetría
        if 'telemetry' in record.getMessage().lower():
            return False
        if 'capture()' in record.getMessage():
            return False
        # Silenciar warnings de IDs duplicados
        if 'Add of existing embedding ID' in record.getMessage():
            return False
        if 'Number of requested results' in record.getMessage():
            return False
        return True

# Aplicar filtro a todos los loggers de ChromaDB
for logger_name in ['chromadb', 'chromadb.telemetry', 'chromadb.db']:
    logger = logging.getLogger(logger_name)
    logger.addFilter(ChromaDBWarningFilter())
    logger.setLevel(logging.ERROR)
