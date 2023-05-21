import os
import zipfile

def listar_archivos_zip(carpeta):
    archivos_zip = []
    for archivo in os.listdir(carpeta):
        if archivo.lower().endswith('.zip'):
            archivos_zip.append(os.path.join(carpeta, archivo))
    return archivos_zip

def crear_ficheros_json_del_zip(archivo_zip, rel_path = "."):
    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        for nombre_archivo in zip_ref.namelist():
            if nombre_archivo.lower().endswith('.json'):
                path = Path(rel_path).joinpath(nombre_archivo)
                path.parent.mkdir(parents=True, exist_ok=True)
                zip_ref.extract(nombre_archivo, rel_path)