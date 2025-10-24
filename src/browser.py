from playwright.sync_api import sync_playwright

def get_browser(headless=False):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    return p, browser
