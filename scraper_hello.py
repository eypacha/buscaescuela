from playwright.sync_api import sync_playwright

url = 'https://example.com'

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    # Extrae el título de la página
    title = page.title()
    print(f'Título de la página: {title}')
    browser.close()
