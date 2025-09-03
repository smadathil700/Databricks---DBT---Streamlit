with source as (
    select * from {{ source('default', 'source_data') }}
),

renamed as (
    select
        VisitorType,
        DeviceType,
        Month,
        Region,
        BounceRates,
        ExitRates,
        product_view,
        add_to_cart,
        purchase,
        case when Revenue=TRUE then 1 else 0 end as Revenue,
        PageValues,
        Administrative_Duration,
        Informational_Duration,
        ProductRelated_Duration
    from source
)

select * from renamed
