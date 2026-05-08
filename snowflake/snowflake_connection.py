import os
import config

from sqlalchemy import create_engine
from urllib.parse import quote_plus

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")

SNOWFLAKE_PASSWORD = quote_plus(
    os.getenv("SNOWFLAKE_PASSWORD")
)

SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")

SNOWFLAKE_WAREHOUSE = os.getenv(
    "SNOWFLAKE_WAREHOUSE",
    "COMPUTE_WH"
)

SNOWFLAKE_DATABASE = os.getenv(
    "SNOWFLAKE_DATABASE",
    "RETAIL_WAREHOUSE"
)

SNOWFLAKE_SCHEMA = os.getenv(
    "SNOWFLAKE_SCHEMA",
    "RAW"
)

SNOWFLAKE_ROLE = os.getenv(
    "SNOWFLAKE_ROLE",
    "ACCOUNTADMIN"
)

connection_string = (
    f"snowflake://{SNOWFLAKE_USER}:{SNOWFLAKE_PASSWORD}"
    f"@{SNOWFLAKE_ACCOUNT}/"
    f"{SNOWFLAKE_DATABASE}/{SNOWFLAKE_SCHEMA}"
    f"?warehouse={SNOWFLAKE_WAREHOUSE}"
    f"&role={SNOWFLAKE_ROLE}"
)

engine = create_engine(connection_string)