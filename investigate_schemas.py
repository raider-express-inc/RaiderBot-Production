#!/usr/bin/env python3
"""
Investigate available schemas in Snowflake account
"""

import os
import sys

sys.path.append(os.path.dirname(__file__))

from src.snowflake.cortex_analyst_client import cortex_client


def investigate_schemas():
    """Query available schemas in the Snowflake account"""
    print("🔍 Investigating available schemas in Snowflake account...")
    print("=" * 60)

    try:
        cortex_client.ensure_connection()
        print("✅ Connection established successfully")

        print("\n1️⃣ Available databases:")
        databases = cortex_client.execute_query("SHOW DATABASES")
        for db in databases[:10]:  # Show first 10
            print(f"   📁 {db.get('name', 'Unknown')}")

        print(
            f"\n2️⃣ Available schemas in database '{cortex_client.config.get('database')}':"
        )
        schemas = cortex_client.execute_query("SHOW SCHEMAS")
        for schema in schemas[:20]:  # Show first 20
            schema_name = schema.get("name", "Unknown")
            print(f"   📂 {schema_name}")

        print("\n3️⃣ Schemas containing 'MCLEOD' or 'DB':")
        mcleod_schemas = [
            s
            for s in schemas
            if "MCLEOD" in s.get("name", "").upper()
            or "DB" in s.get("name", "").upper()
        ]
        if mcleod_schemas:
            for schema in mcleod_schemas:
                schema_name = schema.get("name", "Unknown")
                print(f"   🎯 {schema_name}")
        else:
            print("   ❌ No schemas found containing 'MCLEOD' or 'DB'")

        print("\n4️⃣ Looking for ORDERS table in available schemas:")
        for schema in schemas[:10]:
            schema_name = schema.get("name", "Unknown")
            try:
                tables = cortex_client.execute_query(
                    f"SHOW TABLES IN SCHEMA {schema_name}"
                )
                orders_tables = [
                    t for t in tables if "ORDER" in t.get("name", "").upper()
                ]
                if orders_tables:
                    print(
                        f"   ✅ Schema '{schema_name}' contains order-related tables:"
                    )
                    for table in orders_tables:
                        print(f"      📋 {table.get('name', 'Unknown')}")
            except Exception as e:
                print(f"   ❌ Cannot access schema '{schema_name}': {str(e)[:100]}")

    except Exception as e:
        print(f"❌ Investigation failed: {e}")
        return False

    return True


if __name__ == "__main__":
    investigate_schemas()
