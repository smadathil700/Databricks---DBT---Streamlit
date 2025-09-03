WITH source AS (
  SELECT *
  FROM {{ ref('stg_source') }}
)

SELECT
  product_view,
  add_to_cart,
  purchase,
  BounceRates,
  ExitRates,
  PageValues,
  Administrative_Duration,
  Informational_Duration,
  ProductRelated_Duration,
  VisitorType,
  Month,
  Region
FROM source