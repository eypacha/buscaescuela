def extract_email(page_content):
    import re
    match = re.search(r'[\w\.-]+@[\w\.-]+', page_content)
    return match.group(0) if match else None
