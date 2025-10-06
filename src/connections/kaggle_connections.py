import logging
from pathlib import Path
import shutil
import zipfile
import kagglehub



# ----------------------------
# Constantes de carpetas
# ----------------------------
ROOT_DIR = Path.cwd()
DATA_DIR = Path(f"{ROOT_DIR}/data")
ARCHIVES_DIR = Path(f"{DATA_DIR}/archives")
RAW_DIR = Path(f"{DATA_DIR}/raw")

class KaggleHubClient:
    """Cliente simple para trabajar con kagglehub y redirigir archivos al proyecto.


    Métodos principales:
    - download_dataset(slug): descarga vía kagglehub y devuelve la carpeta origen (caché)
    - archive_dataset(folder_dir): crea un ZIP en data/archives desde `folder_dir`
    - sync_to_raw(folder_dir): copia `folder_dir` a data/raw/<owner-dataset>/
    """

    def __init__(self,
                archives_dir: Path | str = ARCHIVES_DIR,
                raw_dir: Path | str = RAW_DIR) -> None:
        self.archives_dir = Path(archives_dir)
        self.raw_dir = Path(raw_dir)

    def download_dataset(self, slug: str) -> Path:
        """Descarga dataset a la **caché** de kagglehub y devuelve la carpeta local.
        Ej.: slug="ayeshasiddiqa123/coffee-dataset""
        """
        _logger.info(f"Descargando con kagglehub: {slug}" )
        path_str = kagglehub.dataset_download(slug)
        folder_dir = Path(path_str)
        if not folder_dir.exists():
            raise FileNotFoundError(f"kagglehub devolvió una ruta inexistente:{folder_dir}")
        _logger.info(f"Descargado en caché local: {folder_dir}")
        return folder_dir

    def copy_to_archives_then_raw(self, folder_dir: Path | str) -> list[Path]:
        folder_dir_path = Path(folder_dir)
        if not folder_dir_path.exists():
            raise FileNotFoundError(f"No existe la carpeta : {folder_dir_path}")
        archivos_extraidos=list(folder_dir_path.glob("*"))
        for archivo in archivos_extraidos:
            _logger.info(f"Procesando {archivo}")
            archivo_str = str(archivo.name).replace(" ", "_")
            archivo_destino = archivo.with_name(archivo_str)

            created_in_raw: list[Path] = []    
            if not archivo.is_file():
                continue
            else:
                # 1) Copia SIEMPRE a archives
                dest_arch=Path(f"{ARCHIVES_DIR}/{archivo_destino.name}")
                _logger.info(f"Copiando a archives : {archivo.name} -> {dest_arch}" )
                shutil.copy2(archivo, dest_arch)
                # 2) UNZIP ZIP a raw
                if archivo.suffix.lower() == ".zip":
                    target_dir = Path(f"{RAW_DIR}/{archivo_destino.name} ") # RAW_DIR / archivo.name # carpeta con el nombre del zip
                    _logger.info(f"Unzipping {archivo.name} -> {target_dir}" )
                    with zipfile.ZipFile(archivo, "r") as zf:
                        zf.extractall(target_dir)
                        created_in_raw.append(target_dir)
                # 3) Envia archivos a raw
                else:
                    dest_raw = Path(f"{RAW_DIR}/{archivo_destino.name}")
                    _logger.info(f"Copiando a RAW : {archivo.name} -> {dest_raw}" )
                    shutil.copy2(archivo, dest_raw)
                    created_in_raw.append(dest_raw)
                    
        _logger.info("Ingesta completada. Elementos creados en RAW: %d", len(created_in_raw))
        return created_in_raw

    
# ----------------------------
# Configuración de logging
# ----------------------------
_logger = logging.getLogger(__name__)
if not _logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    _logger.addHandler(handler)
_logger.setLevel(logging.INFO)