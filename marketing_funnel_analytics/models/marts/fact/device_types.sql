with source as (
    select * from {{ ref("stg_source") }}
),

device_data as (

    select
        DeviceType as device_type,
        sum(purchase) as purchases,
        count(*) as sessions,
        round(sum(purchase)/count(*),2) as conversion_rate
    from 
        source
    group by
        DeviceType

)

select * from device_data