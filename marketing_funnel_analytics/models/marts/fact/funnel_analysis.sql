WITH source AS (
  SELECT *
  FROM {{ ref('inter_funnel_steps') }}
),

funnel as (
SELECT
  website_visits,
  product_views,
  add_to_cart,
  purchases,
  ROUND(purchases * 1.0 / website_visits, 4) AS conversion_rate,
  website_visits - product_views AS drop_off,
  ROUND((website_visits - product_views) * 1.0 / website_visits, 4) AS drop_off_rate
FROM source
)

select * from funnel