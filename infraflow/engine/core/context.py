from dataclasses import dataclass

@dataclass
class RepairContext:
    db_pool: object
    redis: object
