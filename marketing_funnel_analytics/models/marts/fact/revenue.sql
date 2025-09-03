with source as (
    select * from {{ ref('stg_source') }}
),

selected as (
SELECT
  ROUND(SUM(Revenue), 2) AS total_revenue,
  ROUND(AVG(Revenue), 2) AS average_order_value
FROM source
WHERE Revenue = 1
)

select * from selected