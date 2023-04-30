#!/usr/bin/env python

import os
import zipfile
import json
import logging
from pathlib import Path
from exif import Image, DATETIME_STR_FORMAT
from datetime import datetime
import time
import pywintypes
import win32file

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

def cargar_takeout_json(archivo_json):

    PHOTO_TAKEN_TIME_TAG = "photoTakenTime"
    TIMESTAMP_TAG = "timestamp"
    TITLE_TAG = "title"
    GEO_DATA_EXIF_TAG = "geoDataExif"
    LATITUDE_TAG = "latitude"
    LONGITUDE_TAG = "longitude"
    ALTITUDE_TAG = "altitude"

    with open(archivo_json, 'r', encoding='utf-8') as file:
        tags = {}
        data = {}

        try:
            data = json.load(file)
        except Exception as e:
            logging.error(f"Error procesando {archivo_json} la excepción es: {e}")
        
        if PHOTO_TAKEN_TIME_TAG in data:
            tags[TIMESTAMP_TAG] = int(data[PHOTO_TAKEN_TIME_TAG][TIMESTAMP_TAG])
        
        if TITLE_TAG in data:
            tags[TITLE_TAG] = data[TITLE_TAG]
        
        if GEO_DATA_EXIF_TAG in data:
            tags[LATITUDE_TAG] = data[GEO_DATA_EXIF_TAG][LATITUDE_TAG]
            tags[LONGITUDE_TAG] = data[GEO_DATA_EXIF_TAG][LONGITUDE_TAG]
            tags[ALTITUDE_TAG] = data[GEO_DATA_EXIF_TAG][ALTITUDE_TAG]

    return tags

def aplicar_tags_imagen(tags,archivo_imagen):

    with open(archivo_imagen, 'rb') as image_file:
        my_image = Image(image_file)
    
    datetime_original = datetime.fromtimestamp(tags["timestamp"])
    my_image.datetime_original = datetime_original.strftime(DATETIME_STR_FORMAT)

    with open(archivo_imagen, 'wb') as image_file:
        image_file.write(my_image.get_file())     

def modificarAtributosDeCreacionModificacionYAccesoWin32(ruta_archivo,fecha_en_segundos):

    os.utime(ruta_archivo, (fecha_en_segundos, fecha_en_segundos))

    # Windows Stuff
    fecha_gmtime = time.gmtime(fecha_en_segundos)
    nueva_fecha = pywintypes.Time(fecha_gmtime)

    handle = win32file.CreateFile(
        ruta_archivo,
        win32file.FILE_GENERIC_WRITE,
        0,
        None,
        win32file.OPEN_EXISTING,
        0,
        None,
    )

    descriptor_archivo = handle.handle

    win32file.SetFileTime(descriptor_archivo, nueva_fecha, None, None)
    handle.Close()


def procesarJSONSyAplicaralasImagenes(jsons_dir =".",imagenes_dir = "."):

    for root, dirs, files in os.walk(jsons_dir):
        for file in files:

            archivo_json = os.path.join(root, file)
            tags = cargar_takeout_json(archivo_json)
            TITLE_TAG = "title"

            if TITLE_TAG in tags:
                dir_imagen = imagenes_dir + (root.replace(jsons_dir,""))
                ruta_imagen = os.path.join(dir_imagen,tags[TITLE_TAG])
                
                try:
                    aplicar_tags_imagen(tags,ruta_imagen)
                except Exception:
                    logging.error(f"Problema cob {ruta_imagen} y el json {archivo_json}")
            

if __name__ == "__main__":

    logging.basicConfig(filename='errores.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    encoding='utf-8')

    logging.info("--- INICIA EJECUCIÓN ---");

    imagenes_dir = "C:/Users/artur/OneDrive/Imágenes"
    utilidades_dir = "C:/Users/artur/Desktop/Utilidades"
    subcarpeta_google_fotos = utilidades_dir + "/Takeout/Google Fotos"

    ruta_rel_imagen = "/Photos from 2015/IMG_20150705_105702323.jpg"

    #procesarJSONSyAplicaralasImagenes(subcarpeta_google_fotos,imagenes_dir)

    json_prueba = subcarpeta_google_fotos + ruta_rel_imagen + ".json";
    imagen_prueba = imagenes_dir + ruta_rel_imagen;

    tags = cargar_takeout_json(json_prueba)

    modificarAtributosDeCreacionModificacionYAccesoWin32(imagen_prueba,tags["timestamp"])


    logging.info("--- TERMINA EJECUCIÓN ---");
                    
