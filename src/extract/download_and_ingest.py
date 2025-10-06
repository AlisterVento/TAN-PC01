from pathlib import Path
from src.connections.kaggle_connections import KaggleHubClient
import logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
ROOT_DIR = Path.cwd()
def main():
    # 1) Define el slug del dataset (owner/dataset)
    # Ejemplo: "zynicide/wine-reviews" o "robikscube/medical-insurance-cost"
    slug = "ahmedabbas757/coffee-sales"  # <-- cambia esto por el que vayas a usar

    client = KaggleHubClient()
    # 2) Descarga a la caché local de kagglehub y devuelve la carpeta
    cache_dir: Path = client.download_dataset(slug)

    # 3) Copia a archives y deja el contenido listo en raw (descomprime zips)
    created = client.copy_to_archives_then_raw(cache_dir)

    logger.info("Elementos creados en RAW:")
    for p in created:
        logger.info(" - %s", p)

if __name__ == "__main__":
    main()