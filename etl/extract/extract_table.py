import config
import os
import pandas as pd

from etl.db_connection import engine

RAW_DATA_DIR = "data/raw"

def extract_table(table_name):

    print(f"\nStarting extraction for: {table_name}")

    query = f"SELECT * FROM {table_name}"

    df = pd.read_sql(query, engine)

    output_path = os.path.join(
        RAW_DATA_DIR,
        f"{table_name}.csv"
    )

    df.to_csv(output_path, index=False)

    print(f"Extracted {len(df)} rows from {table_name}")
    print(f"Saved to {output_path}")

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
        extract_table(table)

    print("\nAll extractions completed.")