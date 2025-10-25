def extract_email(page_content):
    import re
    matches = re.findall(r'[\w\.-]+@[\w\.-]+', page_content)
    valid_domains = [
        '.com', '.ar', '.edu', '.org', '.net', 'gmail', 'hotmail', 'yahoo', 'outlook', 'gob', 'edu.ar', 'live', 'icloud'
    ]
    for email in matches:
        if any(domain in email.lower() for domain in valid_domains):
            return email
    return None
