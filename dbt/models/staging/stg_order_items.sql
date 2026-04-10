with source as (
    select * from {{ source('raw', 'order_items') }}
),

products as (
    select * from {{ source('raw', 'products') }}
)

select
    oi.order_item_id,
    oi.created_at,
    oi.order_id,
    oi.product_id,
    p.product_name,
    case
        when cast(oi.is_primary_item as varchar) in ('1', 'MQ==', 'true', 'TRUE', 't')
            then true
        else false
    end as is_primary_item,
    oi.price_usd,
    oi.cogs_usd,
    oi.price_usd - oi.cogs_usd as margin_usd
from source oi
left join products p on oi.product_id = p.product_id
