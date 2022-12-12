import os

ROOT = os.path.dirname(__file__)
DATASET_ROOT = os.path.abspath(os.path.join(ROOT, "files", "datasets_final"))
FILES_ROOT = os.path.abspath(os.path.join(ROOT, "files"))
IMAGES_ROOT = os.path.abspath(os.path.join(ROOT, "files", "images"))
USUARIOS_ROOT = os.path.abspath(os.path.join(ROOT, "usuarios.json"))
ESTADISTICA_ROOT = os.path.abspath(os.path.join(ROOT,"estadistica"))

DIFICULTADES_DEFAULT = {
    "facil": {
        "rondas": 5,
        "tiempo": 65,
        "acierto": 8,
        "error": 0,
        "pistas": 5
    },
    "normal": {
        "rondas": 8,
        "tiempo": 45,
        "acierto": 10,
        "error": 2,
        "pistas": 4
    },
    "dificil": {
        "rondas": 10,
        "tiempo": 30,
        "acierto": 10,
        "error": 5,
        "pistas": 3
    },
    "experto": {
        "rondas": 12,
        "tiempo": 15,
        "acierto": 12,
        "error": 7,
        "pistas": 2
    }}