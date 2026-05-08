import config
import pandas as pd

from etl.db_connection import engine

# Query data
query = """
SELECT *
FROM customers
"""

# Load into DataFrame
df = pd.read_sql(query, engine)

# Preview
print(df.head())

# Export locally
output_path = "etl/extract/customers.csv"

df.to_csv(output_path, index=False)

print(f"\nExtracted {len(df)} customers.")
print(f"Saved to {output_path}")