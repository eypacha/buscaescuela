#!/bin/bash
# Script de desarrollo: borra escuelas.txt y ejecuta el scraper

rm -f escuelas.txt
source .venv/bin/activate
python -m src.main
