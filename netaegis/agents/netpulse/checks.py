import re
import socket
import subprocess


def ping_host(ip: str, count: int = 1) -> float | None:
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), ip],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        if result.returncode == 0:
            match = re.search(r"time=(\d+\.?\d*) ms", result.stdout)
            if match:
                return float(match.group(1))
    except Exception:
        return None
    return None


def check_port(ip: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except Exception:
        return False
