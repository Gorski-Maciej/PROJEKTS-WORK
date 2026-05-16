from datetime import datetime, timezone
from api.core.database import SessionLocal, Base, engine
from api.models.entities import Tenant, CostRecord


def main() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        tenant = db.query(Tenant).filter(Tenant.name == "demo").first()
        if tenant is None:
            tenant = Tenant(name="demo")
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
        db.add_all([
            CostRecord(tenant_id=tenant.id, provider="aws", service="ec2", resource_id="i-demo-1", amount_usd=120.0, usage_quantity=14, collected_at=datetime.now(timezone.utc)),
            CostRecord(tenant_id=tenant.id, provider="azure", service="vm", resource_id="vm-demo-1", amount_usd=90.0, usage_quantity=10, collected_at=datetime.now(timezone.utc)),
        ])
        db.commit()
        print("Demo data seeded")
    finally:
        db.close()


if __name__ == "__main__":
    main()
