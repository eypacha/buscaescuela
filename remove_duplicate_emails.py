#!/usr/bin/env python3
import csv

input_file = 'escuelas.csv'
output_file = 'escuelas_curated.csv'

seen_emails = set()
rows = []

with open(input_file, 'r', encoding='utf-8') as infile:
    reader = csv.reader(infile)
    for row in reader:
        if len(row) < 3:
            continue 
        email = row[2].strip().lower()
        if email and email not in seen_emails:
            seen_emails.add(email)
            rows.append(row)

with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.writer(outfile, quoting=csv.QUOTE_MINIMAL)
    writer.writerows(rows)

print(f"Filtrado completado. Guardado en {output_file}.")
