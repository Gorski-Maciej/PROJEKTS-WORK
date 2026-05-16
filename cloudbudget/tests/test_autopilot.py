from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.core.database import Base
from api.models.entities import Tenant, Recommendation
from api.services.autopilot_service import eligible_autopilot_recommendations, mark_recommendations_approved


def test_autopilot_eligibility_and_apply():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    db.add_all([Tenant(id=1, name="tenant1"), Tenant(id=2, name="tenant2")])
    db.add_all([
        Recommendation(tenant_id=1, category="rightsizing", resource_id="r1", confidence=0.95, estimated_savings_usd=120, approved=False, note=""),
        Recommendation(tenant_id=1, category="rightsizing", resource_id="r2", confidence=0.70, estimated_savings_usd=120, approved=False, note=""),
        Recommendation(tenant_id=2, category="rightsizing", resource_id="r3", confidence=0.99, estimated_savings_usd=200, approved=False, note=""),
    ])
    db.commit()

    eligible = eligible_autopilot_recommendations(db, 1)
    assert len(eligible) == 1

    updated = mark_recommendations_approved(db, 1, [eligible[0].id, 9999])
    assert updated == 1
    assert db.query(Recommendation).filter(Recommendation.id == eligible[0].id).first().approved is True
    # cross-tenant recommendation must remain unchanged
    assert db.query(Recommendation).filter(Recommendation.tenant_id == 2).first().approved is False
