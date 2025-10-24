from rich import print
from src.browser import get_browser
from src.extractors import extract_email
from playwright.sync_api import TimeoutError
from urllib.parse import urljoin

LABEL_WIDTH = 14

def main():
    url = 'https://buscatuescuela.buenosaires.gob.ar'
    p, browser = get_browser(headless=False)
    context = browser.new_context()
    def block_resources(route, request):
        if request.resource_type in ["image", "media", "font", "stylesheet"]:
            route.abort()
        else:
            route.continue_()
    context.route("**/*", block_resources)
    page = context.new_page()
    print(f"[bold cyan]{'Navegando a:':<{LABEL_WIDTH}}[/bold cyan] {url}")
    page.goto(url, timeout=10000, wait_until="domcontentloaded")
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


    # Obtener todos los hrefs de los enlaces de escuelas
    a_tags = page.query_selector_all('.col-sm-6.col-lg-6 > a')
    hrefs = [a.get_attribute('href').strip() for a in a_tags if a.get_attribute('href')]

    for idx, href in enumerate(hrefs, 1):
        print(f"[green]{'URL:':<{LABEL_WIDTH}}[/green] {href}")
        if href:
            if not href.startswith('http'):
                next_url = urljoin(url, href)
            else:
                next_url = href
            page.goto(next_url, timeout=60000, wait_until="domcontentloaded")

            nombre = ''
            try:
                nombre = page.inner_text('h2')
                print(f"[bold magenta]{'Nombre:':<{LABEL_WIDTH}}[/bold magenta] {nombre}")
            except Exception as e:
                print(f"[red]No se encontró ningún h2:[/red] {e}")

            page_content = page.content()
            mail = extract_email(page_content)

            print(f"[bold blue]{'Mail:':<{LABEL_WIDTH}}[/bold blue] {mail if mail else ''}")
            nueva_linea = f'{idx},{nombre if nombre else ""},{mail if mail else ""}\n'
            try:
                with open('escuelas.csv', 'r', encoding='utf-8') as f:
                    existentes = f.readlines()
            except FileNotFoundError:
                existentes = []
            if nueva_linea not in existentes:
                with open('escuelas.csv', 'a', encoding='utf-8') as f:
                    f.write(nueva_linea)
            if not mail:
                print("[red]No se encontró ningún mail en la página.[/red]")

            # Volver a la página de resultados para el siguiente enlace
            page.go_back(wait_until="domcontentloaded")
            page.wait_for_selector('.col-sm-6.col-lg-6 > a')

    browser.close()
    p.stop()

if __name__ == "__main__":
    main()
