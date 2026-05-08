WITH ranked_customers AS (

    SELECT
        customer_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        LOWER(email) AS email,
        city,
        created_at,

        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY created_at DESC
        ) AS row_num

    FROM RETAIL_WAREHOUSE.RAW.customers

)

SELECT
    customer_id,
    first_name,
    last_name,
    email,
    city,
    created_at

FROM ranked_customers

WHERE row_num = 1