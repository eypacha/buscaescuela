LABEL_WIDTH = 14
from rich import print
from src.browser import get_browser
from src.extractors import extract_email
from playwright.sync_api import TimeoutError
from urllib.parse import urljoin

def main():
    url = 'https://buscatuescuela.buenosaires.gob.ar'
    p, browser = get_browser(headless=False)
    page = browser.new_page()
    print(f"[bold cyan]{'Navegando a:':<{LABEL_WIDTH}}[/bold cyan] {url}")
    page.goto(url, timeout=10000)
    try:
        page.wait_for_selector('#barrio_id', timeout=20000)
    except TimeoutError as e:
        print(f"[bold red]No se encontró #barrio_id:[/bold red] {e}")
        with open('debug_pagina.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("[yellow]HTML guardado en debug_pagina.html[/yellow]")
        browser.close()
        p.stop()
        return

    page.select_option('#barrio_id', value='47')
    page.click('button.btn.btn-lg.btn-primary.btn-block.mt-5')
    page.wait_for_selector('.listado a')

    primer_href = page.get_attribute('.listado a', 'href')
    print(f"[green]{'URL:':<{LABEL_WIDTH}}[/green]{primer_href}")

    if primer_href:
        if not primer_href.startswith('http'):
            next_url = urljoin(url, primer_href)
        else:
            next_url = primer_href
        page.goto(next_url, timeout=60000)

        primer_h2 = ''
        try:
            primer_h2 = page.inner_text('h2')
            print(f"[bold magenta]{'Nombre:':<{LABEL_WIDTH}}[/bold magenta] {primer_h2}")
        except Exception as e:
            print(f"[red]No se encontró ningún h2:[/red] {e}")

        page_content = page.content()
        primer_mail = extract_email(page_content)
        if primer_mail:
            print(f"[bold blue]{'Mail:':<{LABEL_WIDTH}}[/bold blue] {primer_mail}")
        else:
            print("[red]No se encontró ningún mail en la página.[/red]")

        with open('escuelas.csv', 'a', encoding='utf-8') as f:
            f.write(f'{primer_h2},{primer_mail}\n')

    browser.close()
    p.stop()

if __name__ == "__main__":
    main()
