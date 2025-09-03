with source as (
    select * from {{ ref('inter_session_metrics') }}
),

selected as (
SELECT
  ROUND(SUM(add_to_cart - purchase) * 1.0 / NULLIF(SUM(add_to_cart), 0), 4) AS cart_abandonment_rate
FROM source
)

select * from selected