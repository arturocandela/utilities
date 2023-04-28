#!/usr/bin/env python

import os
import zipfile
import json
import logging
from pathlib import Path
from exif import Image, DATETIME_STR_FORMAT
from datetime import datetime

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

def cargar_json(archivo_json,imagen):
    with open(archivo_json, 'r', encoding='utf-8') as file:
        data = json.load(file)
        timestamp = int(data['photoTakenTime']['timestamp'])
        
        
        image_file = None
        with open(imagen, 'rb') as image_file:
            my_image = Image(image_file)
            
            datetime_original = datetime.fromtimestamp(timestamp)
            my_image.datetime_original = datetime_original.strftime(DATETIME_STR_FORMAT)
            
            with open(imagen, 'wb') as image_file:
                image_file.write(my_image.get_file())

def cargar_takeout_json(archivo_json):
    with open(archivo_json, 'r', encoding='utf-8') as file:
        tags = {}

        try:
            data = json.load(file)
            tags["timestamp"] = int(data['photoTakenTime']['timestamp'])
            tags["title"] = data['title']
        except Exception as e:
            logging.error(f"Error procesando {archivo_json} la excepción es: {e}")
        
        return tags

def aplicar_tags_imagen(tags,archivo_imagen):

    with open(archivo_imagen, 'rb') as image_file:
        my_image = Image(image_file)
    
    datetime_original = datetime.fromtimestamp(tags["timestamp"])
    my_image.datetime_original = datetime_original.strftime(DATETIME_STR_FORMAT)

    with open(archivo_imagen, 'wb') as image_file:
        image_file.write(my_image.get_file())     

def procesarJSONSyAplicaralasImagenes():

    utilidades_dir = "."    
    subcarpeta_google_fotos = "/Takeout/Google Fotos"

    jsons_dir = utilidades_dir + subcarpeta_google_fotos

    subcarpeta = "/Vacaciones 09"
    oneDriveImagenes = "C:/Users/artur/OneDrive/Imágenes"

    # for archivo in os.listdir(jsons_dir + subcarpeta):
    #         if archivo.lower().endswith('.json'):
                
    #             try:
    #                 archivo_jpg = oneDriveImagenes + subcarpeta + "/" + archivo.replace(".json","")
    #                 archivo_json = carpeta_backup + subcarpeta + "/" + archivo
    #                 cargar_json(archivo_json,archivo_jpg)
    #             except Exception as e:
    #                 print(f"Error en: {archivo} error: {e}" )
    #                 logging.error(f"Error en: {archivo} error: {e}")

    for root, dirs, files in os.walk(jsons_dir):
        for file in files:
            ruta_relativa_json = os.path.join(root, file)

            print(f"JSON encontrado: {ruta_relativa_json}")
        
            tags = cargar_takeout_json(ruta_relativa_json)
            TITLE_TAG = "title"

            if TITLE_TAG in tags:
                dir_imagen = oneDriveImagenes + (root.replace(utilidades_dir + subcarpeta_google_fotos,""))
                ruta_imagen = os.path.join(dir_imagen,tags[TITLE_TAG])
                
                try:
                    aplicar_tags_imagen(tags,ruta_imagen)
                except Exception as e:
                    logging.error(f"Problema en: {ruta_imagen} problema: {e}")
            


if __name__ == "__main__":

    logging.basicConfig(filename='errores.log',
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

    logging.info("--- TERMINA EJECUCIÓN ---");

    one_drive_dir = Path("C:/Users/artur/OneDrive")
    utilidades_dir = Path("D:/")
    
    archivos_zip = listar_archivos_zip(one_drive_dir.joinpath("Google Fotos Backup"))

    
    for archivo_zip in archivos_zip:
        logging.info("Procesando ZIP: " + archivo_zip)
        with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
            zip_ref.extractall(utilidades_dir)

        
    
    logging.info("--- TERMINA EJECUCIÓN ---");
                    
