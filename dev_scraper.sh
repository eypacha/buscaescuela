#!/bin/bash
# Script de desarrollo: borra escuelas.csv y ejecuta el scraper

rm -f escuelas.csv
source .venv/bin/activate
python -m src.main
