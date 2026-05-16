import re

FAILED_LOGIN = re.compile(r"Failed password for .* from (?P<ip>\d+\.\d+\.\d+\.\d+)")

def parse_line(line: str) -> dict | None:
    match = FAILED_LOGIN.search(line)
    if match:
        return {"type": "failed_login", "details": {"ip": match.group("ip"), "count": 1}}
    return None
