{{ config(materialized='table') }}

select
  tenant_id,
  provider,
  cast(occurred_at as date) as cost_date,
  sum(amount_usd) as total_amount_usd,
  count(*) as events_count
from cost_events
group by 1,2,3
