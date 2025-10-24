from playwright.sync_api import sync_playwright

url = 'https://buscatuescuela.buenosaires.gob.ar'

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # headless=False para ver la acción
    page = browser.new_page()
    print(f"Navegando a {url}")

    page.goto(url, timeout=10000)
    print("Página cargada, esperando #barrio_id ...")
    try:
        page.wait_for_selector('#barrio_id', timeout=20000)
        print("#barrio_id encontrado!")
    except Exception as e:
        print(f"No se encontró #barrio_id: {e}")
        # Guardar el HTML para inspección
        with open('debug_pagina.html', 'w', encoding='utf-8') as f:
            f.write(page.content())
        print("HTML guardado en debug_pagina.html")
        browser.close()
        exit(1)

    # Espera a que el select esté disponible y selecciona la opción con value '47'
    print("Seleccionando barrio...")
    page.select_option('#barrio_id', value='47')

    # Haz click en el botón de buscar
    print("Clic en buscar...")
    page.click('button.btn.btn-lg.btn-primary.btn-block.mt-5')

    # Espera a que aparezca el listado y el primer enlace dentro
    print("Esperando resultados...")
    page.wait_for_selector('.listado a')

    # Obtiene el href del primer <a> dentro de .listado
    primer_href = page.get_attribute('.listado a', 'href')
    print(f"Primer href encontrado: {primer_href}")

    # Navega al primer enlace encontrado
    if primer_href:
        from urllib.parse import urljoin
        if not primer_href.startswith('http'):
            next_url = urljoin(url, primer_href)
        else:
            next_url = primer_href
        print(f"Navegando a {next_url}")
        page.goto(next_url, timeout=60000)

        # Imprime el primer h2
        try:
            primer_h2 = page.inner_text('h2')
            print(f"Nombre: {primer_h2}")
        except Exception as e:
            print(f"No se encontró ningún h2: {e}")

        # Busca el primer mail en la página
        import re
        page_content = page.content()
        match = re.search(r'[\w\.-]+@[\w\.-]+', page_content)
        if match:
            print(f"Mail: {match.group(0)}")
        else:
            print("No se encontró ningún mail en la página.")
