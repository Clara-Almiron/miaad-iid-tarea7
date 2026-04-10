with source as (
    select * from {{ source('raw', 'website_sessions') }}
)

select
    website_session_id,
    created_at,
    user_id,
    case
        when cast(is_repeat_session as varchar) in ('1', 'MQ==', 'true', 'TRUE', 't')
            then true
        else false
    end as is_repeat_session,
    coalesce(utm_source, 'direct') as utm_source,
    coalesce(utm_campaign, 'none') as utm_campaign,
    utm_content,
    device_type,
    http_referer,
    date_trunc('day', created_at) as session_date,
    date_trunc('week', created_at) as session_week,
    date_trunc('month', created_at) as session_month,
    extract(year from created_at) as session_year
from source
