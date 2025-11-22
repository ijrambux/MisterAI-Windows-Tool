import re

def extract_emails_only(path):
    emails = set()
    pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            for email in pattern.findall(line):
                emails.add(email)

    return list(emails)
