def recommend_ri_plan(monthly_on_demand_cost: float, commitment_years: int = 1) -> dict:
    if commitment_years == 3:
        discount = 0.42
    else:
        discount = 0.28
    reserved_cost = monthly_on_demand_cost * (1 - discount)
    yearly_savings = (monthly_on_demand_cost - reserved_cost) * 12
    return {
        "commitment_years": commitment_years,
        "discount_pct": round(discount * 100, 2),
        "estimated_monthly_reserved_cost": round(reserved_cost, 2),
        "estimated_yearly_savings": round(yearly_savings, 2),
    }
