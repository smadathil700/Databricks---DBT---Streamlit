with source as (
    select * from {{ ref('inter_session_metrics') }}
),

selected as (
SELECT
  purchase,
  ROUND(AVG(PageValues), 2) AS avg_page_value,
  ROUND(AVG(Administrative_Duration), 2) AS avg_admin_duration,
  ROUND(AVG(Informational_Duration), 2) AS avg_info_duration,
  ROUND(AVG(ProductRelated_Duration), 2) AS avg_product_duration
FROM source
GROUP BY purchase
)

select * from selected