def categorize(service: str, amount: float) -> tuple[str, float, float]:
    service_l = service.lower()
    if "storage" in service_l:
        return "unattached_volume", 0.72, amount * 0.15
    if "db" in service_l or "rds" in service_l:
        return "reserved_instance", 0.81, amount * 0.22
    return "rightsizing", 0.78, amount * 0.2
