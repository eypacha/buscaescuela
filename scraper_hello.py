from playwright.sync_api import sync_playwright
import re

url = 'https://buscatuescuela.buenosaires.gob.ar'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False para ver la acción
    page = browser.new_page()
    print(f"Navegando a {url}")

    page.goto(url, timeout=10000)
    try:
        page.wait_for_selector('#barrio_id', timeout=20000)
    except Exception as e:
        print(f"No se encontró #barrio_id: {e}")

        with open('debug_pagina.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("HTML guardado en debug_pagina.html")
        browser.close()
        exit(1)

    page.select_option('#barrio_id', value='47')
    page.click('button.btn.btn-lg.btn-primary.btn-block.mt-5')
    page.wait_for_selector('.listado a')

    primer_href = page.get_attribute('.listado a', 'href')
    print(f"URL: {primer_href}")

    if primer_href:
        from urllib.parse import urljoin
        if not primer_href.startswith('http'):
            next_url = urljoin(url, primer_href)
        else:
            next_url = primer_href
        page.goto(next_url, timeout=60000)

        primer_h2 = ''
        try:
            primer_h2 = page.inner_text('h2')
            print(f"Nombre: {primer_h2}")
        except Exception as e:
            print(f"No se encontró ningún h2: {e}")

        page_content = page.content()
        match = re.search(r'[\w\.-]+@[\w\.-]+', page_content)
        primer_mail = match.group(0) if match else ''
        if primer_mail:
            print(f"Mail: {primer_mail}")
        else:
            print("No se encontró ningún mail en la página.")

        with open('escuelas.cvs', 'a', encoding='utf-8') as f:
            f.write(f'{primer_h2},{primer_mail}\n')
