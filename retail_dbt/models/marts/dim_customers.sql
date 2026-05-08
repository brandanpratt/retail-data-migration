SELECT
    customer_id,
    first_name,
    last_name,
    email,
    city
FROM {{ ref('stg_customers') }}