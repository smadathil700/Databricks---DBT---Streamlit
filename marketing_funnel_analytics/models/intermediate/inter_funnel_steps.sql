with source as (
    select * from {{ ref("stg_source") }}
),

selected as (
SELECT
  SUM(product_view) AS product_views,
  SUM(add_to_cart) AS add_to_cart,
  SUM(purchase) AS purchases,
  COUNT(*) AS website_visits
FROM source
)

select * from selected