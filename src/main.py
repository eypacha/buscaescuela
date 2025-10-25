#!/usr/bin/env python3
import time
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
MAX_ID = 3000

def get_email_from_website(page, url):
    try:
        page.goto(url, timeout=10000, wait_until="domcontentloaded")
        content = page.content()
        email_from_web = extract_email(content)
        return email_from_web
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
            writer.writerow(["id", "name", "email", "management", "level", "web", "web_email"])

    for school_id in range(START_ID, MAX_ID + 1):
        url = f"{BASE_URL}{school_id}"
        print(f"[cyan]Consultando:[/cyan] {url}")
        try:
            page.goto(url, timeout=10000, wait_until="domcontentloaded")
        except Exception as e:
            print(f"[red]Navigation error in ID {school_id}: {e}. Skipping...[/red]")
            continue
        page_content = page.content()
        lower_content = page_content.lower()
        if "server error" in lower_content or "not found" in lower_content:
            print(f"[yellow]Server Error o Not Found en ID {school_id}, saltando...[/yellow]")
            continue
        name = ""
        try:
            name = page.inner_text('h2')
            print(f"[magenta]Nombre:[/magenta] {name}")
        except Exception as e:
            print(f"[red]No se encontró ningún h2 en ID {school_id}:[/red] {e}")
        email = extract_email(page_content)
        print(f"[blue]Mail:[/blue] {email if email else ''}")

        soup = BeautifulSoup(page_content, "html.parser")
        web = ""
        for span in soup.find_all("span"):
            urls = re.findall(r'(https?://[\w\.-]+(?:\.[\w\.-]+)+(?:/[\w\-\./?%&=]*)?|www\.[\w\.-]+(?:\.[\w\.-]+)+(?:/[\w\-\./?%&=]*)?)', span.get_text())
            if urls:
                web = urls[0]
                if web.startswith("www."):
                    web = "http://" + web
                break
        print(f"[green]Web:[/green] {web}")
        web_email = ""
        if web:
            if not any(web.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".svg"]):
                web_email = get_email_from_website(page, web)
                print(f"[yellow]Mail extraído de la web:[/yellow] {web_email}")

        management = ""
        level = ""
        secondary_data = soup.find_all("p", class_="secundario-dato")
        if len(secondary_data) >= 3:
            management = secondary_data[0].get_text(strip=True)
            level = secondary_data[2].get_text(strip=True)
        print(f"[cyan]Gestión:[/cyan] {management}")
        print(f"[cyan]Nivel:[/cyan] {level}")

        new_row = [school_id, name, email if email else "", management, level, web, web_email]
        try:
            with open('escuelas.csv', 'r', encoding='utf-8') as f:
                existing_rows = list(csv.reader(f))
        except FileNotFoundError:
            existing_rows = []
        email_lower = (email or '').strip().lower()
        if email_lower and email_lower not in seen_emails:
            with open('escuelas.csv', 'a', encoding='utf-8', newline='') as f:
                writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(new_row)
            seen_emails.add(email_lower)
            if not email:
                print("[red]No se encontró ningún mail en la página.[/red]")

    browser.close()
    p.stop()
    elapsed = time.time() - start_time
    print(f"[bold green]Tiempo total de ejecución: {elapsed:.2f} segundos[/bold green]")

if __name__ == "__main__":
    main()
