#!/usr/bin/env python

import os
import zipfile
import json
import logging
from pathlib import Path
from exif import Image, DATETIME_STR_FORMAT
from datetime import datetime
import time
import subprocess
import pywintypes
import win32file

from zip_utils import listar_archivos_zip,crear_ficheros_json_del_zip

from strings_tags import ALTITUDE_TAG,GEO_DATA_EXIF_TAG,LATITUDE_TAG,LONGITUDE_TAG
from strings_tags import PHOTO_TAKEN_TIME_TAG,TIMESTAMP_TAG,TITLE_TAG



def cargar_takeout_json(archivo_json):

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

def eliminar_tags_image(archivo_imagen):

    with open(archivo_imagen, 'rb') as image_file:
        my_image = Image(image_file)
    
    my_image.delete("datetime_original")

    with open(archivo_imagen, 'wb') as image_file:
        image_file.write(my_image.get_file()) 

def cambiar_fecha_exiftool(ruta_archivo, fecha):
    fecha_formato_exif = fecha.strftime('%Y:%m:%d %H:%M:%S')

    try:
        subprocess.run(
            [
                "exiftool",
                "-DateTimeOriginal=" + fecha_formato_exif,
                "-CreateDate=" + fecha_formato_exif,
                "-ModifyDate=" + fecha_formato_exif,
                "-overwrite_original",
                ruta_archivo,
            ],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error al cambiar la fecha con exiftool: {e}")

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

    fotos_2015 = "/Japón 2015"

    ruta_rel_imagen = fotos_2015 + "/IMG_20150702_104733262.jpg"

    #procesarJSONSyAplicaralasImagenes(subcarpeta_google_fotos,imagenes_dir)

    json_prueba = subcarpeta_google_fotos + ruta_rel_imagen + ".json";
    imagen_prueba = imagenes_dir + ruta_rel_imagen;

    for f in os.listdir(imagenes_dir + fotos_2015):
        f_lower = imagenes_dir + fotos_2015 + "/" + f.lower()
        if f_lower.endswith(".jpg") or f_lower.endswith(".jpeg"):
            imagen_prueba = f_lower
            json_prueba = f_lower + ".json"

            if (Path(json_prueba).exists()):
                eliminar_tags_image(f_lower)
                tags = cargar_takeout_json(json_prueba)
                modificarAtributosDeCreacionModificacionYAccesoWin32(imagen_prueba,tags["timestamp"])
                cambiar_fecha_exiftool(imagen_prueba,datetime.fromtimestamp(tags["timestamp"]))

    logging.info("--- TERMINA EJECUCIÓN ---");
                    
