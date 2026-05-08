import config
import pandas as pd
import time
from datetime import datetime
from sqlalchemy import text

from etl.db_connection import engine as sql_engine
from snowflake.snowflake_connection import engine as snowflake_engine

RAW_DATA_DIR = "data/raw"


def incremental_extract(table_name, timestamp_column):
    try:
        print(f"\nStarting incremental extraction for {table_name}")

        start_time = datetime.now()
        print(f"Start time: {start_time}")

        start_timer = time.time()
        print(f"Timer started at: {start_timer}")

        # Get last loaded timestamp
        metadata_query = f"""
        SELECT last_loaded_timestamp
        FROM RETAIL_WAREHOUSE.STAGING.etl_metadata
        WHERE table_name = '{table_name}'
        """

        metadata_df = pd.read_sql(
            metadata_query,
            snowflake_engine
        )

        last_loaded_timestamp = metadata_df.iloc[0][
            "last_loaded_timestamp"
        ]

        print(f"Last loaded timestamp: {last_loaded_timestamp}")

        # Pull only new rows
        source_query = text(f"""
        SELECT *
        FROM {table_name}
        WHERE {timestamp_column} > :last_loaded_timestamp
        """)

        df = pd.read_sql(
            source_query,
            sql_engine,
            params={
                "last_loaded_timestamp": last_loaded_timestamp
            }
        )

        print(f"Found {len(df)} new rows")

        if len(df) == 0:

            print("No new rows found.")

            end_time = datetime.now()

            duration = time.time() - start_timer

            audit_insert = f"""
            INSERT INTO RETAIL_WAREHOUSE.STAGING.pipeline_audit_log
            VALUES (
                'incremental_extract',
                '{table_name}',
                0,
                'SUCCESS',
                '{start_time}',
                '{end_time}',
                {duration},
                NULL
            )
            """

            with snowflake_engine.begin() as conn:
                conn.execute(text(audit_insert))

            return

        output_path = f"{RAW_DATA_DIR}/{table_name}_incremental.csv"

        df.to_csv(output_path, index=False)

        print(f"Saved incremental extract to {output_path}")

        # Append to Snowflake RAW table
        df.to_sql(
            table_name,
            snowflake_engine,
            schema="RAW",
            if_exists="append",
            index=False
        )

        print(f"Loaded {len(df)} rows into Snowflake")

        # Update metadata timestamp

        update_query = text("""
        UPDATE RETAIL_WAREHOUSE.STAGING.etl_metadata
        SET last_loaded_timestamp = :newest_timestamp
        WHERE table_name = :table_name
        """)

        with snowflake_engine.begin() as conn:
            conn.execute(text(update_query))

        print(f"Updated metadata for {table_name}")

        end_time = datetime.now()

        duration = time.time() - start_timer

        audit_insert = f"""
        INSERT INTO RETAIL_WAREHOUSE.STAGING.pipeline_audit_log
        VALUES (
            'incremental_extract',
            '{table_name}',
            {len(df)},
            'SUCCESS',
            '{start_time}',
            '{end_time}',
            {duration},
            NULL
        )
        """

        with snowflake_engine.begin() as conn:
            conn.execute(text(audit_insert))

    except Exception as e:

        end_time = datetime.now()

        duration = time.time() - start_timer

        error_insert = f"""
        INSERT INTO RETAIL_WAREHOUSE.STAGING.pipeline_audit_log
        VALUES (
            'incremental_extract',
            '{table_name}',
            0,
            'FAILED',
            '{start_time}',
            '{end_time}',
            {duration},
            '{str(e)}'
        )
        """

        with snowflake_engine.begin() as conn:
            conn.execute(text(error_insert))
        raise

if __name__ == "__main__":

    incremental_extract(
        "customers",
        "created_at"
    )

    incremental_extract(
        "orders",
        "order_date"
    )