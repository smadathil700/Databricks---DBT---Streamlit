with source as (
    select * from {{ ref("stg_source") }}
),

funnel as (

    select
        purchase,
        avg(BounceRates) as avg_bounce_rates,
        avg(ExitRates) as avg_exit_rates
    from 
        source
    group by
        purchase

)

select * from funnel