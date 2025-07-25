#!/usr/bin/env python3
"""
Investigate actual table structure in SQL_SERVER_DBO schema
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from src.snowflake.cortex_analyst_client import cortex_client

def investigate_table_structure():
    """Query actual table structure in SQL_SERVER_DBO schema"""
    print("🔍 Investigating table structure in SQL_SERVER_DBO schema...")
    print("=" * 60)
    
    try:
        conn = cortex_client.ensure_connection()
        print("✅ Connection established successfully")
        
        print(f"\n1️⃣ ORDERS table structure:")
        try:
            columns = cortex_client.execute_query("DESCRIBE TABLE SQL_SERVER_DBO.ORDERS")
            print(f"   📋 Found {len(columns)} columns in ORDERS table:")
            for col in columns[:20]:  # Show first 20 columns
                col_name = col.get('name', 'Unknown')
                col_type = col.get('type', 'Unknown')
                print(f"      🔹 {col_name} ({col_type})")
        except Exception as e:
            print(f"   ❌ Cannot describe ORDERS table: {str(e)}")
            
        print(f"\n2️⃣ Sample data from ORDERS table:")
        try:
            sample = cortex_client.execute_query("SELECT * FROM SQL_SERVER_DBO.ORDERS LIMIT 3")
            if sample:
                print(f"   📊 Sample record keys: {list(sample[0].keys())}")
                for i, record in enumerate(sample):
                    print(f"   📝 Record {i+1}: {len(record)} fields")
            else:
                print("   ❌ No sample data found")
        except Exception as e:
            print(f"   ❌ Cannot query sample data: {str(e)}")
            
        print(f"\n3️⃣ Other order-related tables in SQL_SERVER_DBO:")
        order_tables = ['ORDER_MASTER', 'EDI_ORDER', 'MOVEMENT_ORDER']
        for table in order_tables:
            try:
                columns = cortex_client.execute_query(f"DESCRIBE TABLE SQL_SERVER_DBO.{table}")
                print(f"   📋 {table}: {len(columns)} columns")
                col_names = [col.get('name', 'Unknown') for col in columns[:5]]
                print(f"      🔹 First 5 columns: {', '.join(col_names)}")
            except Exception as e:
                print(f"   ❌ Cannot describe {table}: {str(e)[:100]}")
                
    except Exception as e:
        print(f"❌ Investigation failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    investigate_table_structure()
