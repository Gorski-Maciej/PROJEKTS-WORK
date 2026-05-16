import strawberry
from sqlalchemy.orm import Session
from api.core.database import SessionLocal
from api.models.entities import CostRecord


@strawberry.type
class CostSummary:
    provider: str
    total: float


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "cloudbudget-graphql"

    @strawberry.field
    def provider_totals(self, tenant_id: int) -> list[CostSummary]:
        db: Session = SessionLocal()
        try:
            rows = db.query(CostRecord.provider, CostRecord.amount_usd).filter(CostRecord.tenant_id == tenant_id).all()
            totals: dict[str, float] = {}
            for p, a in rows:
                totals[p] = totals.get(p, 0.0) + float(a)
            return [CostSummary(provider=k, total=v) for k, v in totals.items()]
        finally:
            db.close()


schema = strawberry.Schema(query=Query)
