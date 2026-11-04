import logging

def get_logger():
    """
    Configura y devuelve un logger que escribe los eventos en un archivo local.
    """
    logger = logging.getLogger("LabTrackLogger")
    logger.setLevel(logging.INFO)

    # Evitamos añadir múltiples manejadores si se llama a la función varias veces
    if not logger.handlers:
        # FileHandler: Guarda los logs físicamente en la raíz del proyecto
        file_handler = logging.FileHandler("labtrack_system.log", encoding="utf-8")
        
        # Formato: [2026-11-04 10:30:15] - [INFO/ERROR] - [Mensaje]
        formato = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formato)
        
        logger.addHandler(file_handler)

    return logger