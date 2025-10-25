from rich import print
from src.browser import get_browser
from src.extractors import extract_email
from playwright.sync_api import TimeoutError

LABEL_WIDTH = 14

def main():
    BASE_URL = "https://buscatuescuela.buenosaires.gob.ar/establecimientos/show-establecimientos/"
    MAX_ID = 2000  # Cambia este valor según el rango de IDs que quieras probar
    p, browser = get_browser(headless=False)
    context = browser.new_context()
    def block_resources(route, request):
        if request.resource_type in ["image", "media", "font", "stylesheet"]:
            route.abort()
        else:
            route.continue_()
    context.route("**/*", block_resources)
    page = context.new_page()

    for eid in range(1, MAX_ID + 1):
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
        nueva_linea = f'{eid},{nombre},{mail if mail else ""}\n'
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

    browser.close()
    p.stop()

if __name__ == "__main__":
    main()
