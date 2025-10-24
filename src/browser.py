# Funciones relacionadas con la inicialización y helpers de Playwright
from playwright.sync_api import sync_playwright

def get_browser(headless=True):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    return p, browser
