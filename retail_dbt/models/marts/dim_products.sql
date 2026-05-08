SELECT
    product_id,
    product_name,
    category,
    price
FROM {{ ref('stg_products') }}

SELECT *
FROM nonexistent_table