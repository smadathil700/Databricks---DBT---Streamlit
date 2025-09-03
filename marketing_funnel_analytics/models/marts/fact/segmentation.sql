With source as (
    select * from {{ ref('inter_session_metrics') }}
),

selected as (
SELECT
  VisitorType,
  Month,
  SUM(purchase) AS purchases,
  SUM(product_view) AS product_views,
  SUM(add_to_cart) AS add_to_cart,
  ROUND(SUM(purchase) * 1.0 / NULLIF(SUM(product_view), 0), 4) AS conversion_rate
FROM source
GROUP BY VisitorType,Month
)

select * from selected