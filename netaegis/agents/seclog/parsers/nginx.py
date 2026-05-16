import re

HTTP_5XX = re.compile(r'" (?P<status>\d{3}) ')

def parse_line(line: str) -> dict | None:
    match = HTTP_5XX.search(line)
    if match and match.group("status").startswith("5"):
        return {"type": "http_5xx", "details": {"status": match.group("status")}}
    return None
