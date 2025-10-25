
# BuscaEscuela

This project is an automated scraper to collect information about schools in Buenos Aires City from https://buscatuescuela.buenosaires.gob.ar.

## What does it do?
- Iterates over school establishment IDs and extracts:
  - School name
  - Main email
  - Website (if available in the profile)
  - Email extracted from the website (if found)
- Saves results in a CSV file (`escuelas.csv`) with duplicate email control.
- Allows resuming scraping from any ID.
- Includes utility scripts to clean duplicates and curate results.

## Structure
- `src/main.py`: Main scraping script (uses Playwright and BeautifulSoup).
- `remove_duplicate_emails.py`: Script to filter duplicate emails (not needed if you use the main script's deduplication).
- `.venv/`: Recommended virtual environment for dependencies.
- `.gitignore`: Ignores generated files and the virtual environment.
- `escuelas.csv`: Results file.

## Requirements
- Python 3.8+
- Playwright (`pip install playwright` and then `playwright install`)
- BeautifulSoup (`pip install beautifulsoup4`)
- rich (`pip install rich`)

It is recommended to use a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # if you have one, or install dependencies manually
```

## Usage

1. Activate the virtual environment:
   ```sh
   source .venv/bin/activate
   ```
2. Run the scraper:
   ```sh
   python src/main.py
   # or if it has shebang and permissions:
   ./src/main.py
   ```
3. The result will be in `escuelas.csv`.

You can modify `START_ID` and `MAX_ID` in `src/main.py` to control the scraping range.

## Notes
- The script avoids duplicate emails.
- If a website is found in the profile, it tries to extract an email from the main page of that domain.
- The scraping is robust against network errors and broken pages.

## License
MIT
