import os
import pandas as pd

from snowflake.snowflake_connection import engine

RAW_DATA_DIR = "data/raw"

def load_csv_to_snowflake(table_name):

    file_path = os.path.join(
        RAW_DATA_DIR,
        f"{table_name}.csv"
    )

    print(f"\nLoading {table_name} into Snowflake...")

    df = pd.read_csv(file_path)

    df.to_sql(
        table_name,
        engine,
        if_exists="replace",
        index=False
    )

    print(f"Loaded {len(df)} rows into {table_name}")

if __name__ == "__main__":

    tables = [
        "customers",
        "stores",
        "products",
        "orders",
        "order_items",
        "inventory",
        "payments"
    ]

    for table in tables:
        load_csv_to_snowflake(table)

    print("\nSnowflake load complete.")