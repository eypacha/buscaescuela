import time

#!/usr/bin/env python3
from rich import print
from src.browser import get_browser
from src.extractors import extract_email
from playwright.sync_api import TimeoutError
import csv
import re
from bs4 import BeautifulSoup

LABEL_WIDTH = 14
BASE_URL = "https://buscatuescuela.buenosaires.gob.ar/establecimientos/show-establecimientos/"
START_ID = 1 
MAX_ID = 2000 

def get_email_from_website(page, url):
    try:
        page.goto(url, timeout=10000, wait_until="domcontentloaded")
        content = page.content()
        mail = extract_email(content)
        return mail
    except Exception as e:
        print(f"[yellow]No se pudo scrapear mail de {url}: {e}[/yellow]")
        return ""

def main():
    start_time = time.time()
    p, browser = get_browser(headless=False)
    context = browser.new_context()
    def block_resources(route, request):
        if request.resource_type in ["image", "media", "font", "stylesheet"]:
            route.abort()
        else:
            route.continue_()
    context.route("**/*", block_resources)
    page = context.new_page()

    seen_emails = set()
    need_header = False
    try:
        with open('escuelas.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
            if not rows:
                need_header = True
            for row in rows:
                if len(row) >= 3:
                    seen_emails.add(row[2].strip().lower())
    except FileNotFoundError:
        need_header = True

    if need_header:
        with open('escuelas.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["id", "nombre", "email", "web", "mail_web"])

    for eid in range(START_ID, MAX_ID + 1):
        url = f"{BASE_URL}{eid}"
        print(f"[cyan]Consultando:[/cyan] {url}")
        try:
            page.goto(url, timeout=10000, wait_until="domcontentloaded")
        except TimeoutError as e:
            print(f"[red]Timeout en ID {eid}, saltando...[/red]")
            continue
        page_content = page.content()
        lower_content = page_content.lower()
        if "server error" in lower_content or "not found" in lower_content:
            print(f"[yellow]Server Error o Not Found en ID {eid}, saltando...[/yellow]")
            continue
        nombre = ""
        try:
            nombre = page.inner_text('h2')
            print(f"[magenta]Nombre:[/magenta] {nombre}")
        except Exception as e:
            print(f"[red]No se encontró ningún h2 en ID {eid}:[/red] {e}")
        mail = extract_email(page_content)
        print(f"[blue]Mail:[/blue] {mail if mail else ''}")

        # Extraer dirección web solo si está dentro de un <span>
        soup = BeautifulSoup(page_content, "html.parser")
        web = ""
        for span in soup.find_all("span"):
            urls = re.findall(r'https?://[\w\.-]+(?:\.[\w\.-]+)+(?:/[\w\-\./?%&=]*)?', span.get_text())
            if urls:
                web = urls[0]
                break
        print(f"[green]Web:[/green] {web}")
        mail_web = ""
        if web:
            # Solo intentar si la web parece un dominio válido (no imagen, no favicon, etc)
            if not any(web.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]):
                mail_web = get_email_from_website(page, web)
                print(f"[yellow]Mail extraído de la web:[/yellow] {mail_web}")
        nueva_fila = [eid, nombre, mail if mail else "", web, mail_web]
        try:
            with open('escuelas.csv', 'r', encoding='utf-8') as f:
                existentes = list(csv.reader(f))
        except FileNotFoundError:
            existentes = []
        email_lower = (mail or '').strip().lower()
        if email_lower and email_lower not in seen_emails:
            with open('escuelas.csv', 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(nueva_fila)
            seen_emails.add(email_lower)
        if not mail:
            print("[red]No se encontró ningún mail en la página.[/red]")

    browser.close()
    p.stop()
    elapsed = time.time() - start_time
    print(f"[bold green]Tiempo total de ejecución: {elapsed:.2f} segundos[/bold green]")

if __name__ == "__main__":
    main()
