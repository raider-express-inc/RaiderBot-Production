#!/usr/bin/env python3
"""
Inspect actual column names in the orders table
"""

import os
import sys
sys.path.append(os.path.dirname(__file__))

from src.snowflake.cortex_analyst_client import cortex_client

def inspect_orders_columns():
    """Get actual column names and sample data from orders table"""
    print("🔍 Inspecting actual column names in orders table...")
    print("=" * 60)
    
    try:
        conn = cortex_client.ensure_connection()
        print("✅ Connection established successfully")
        
        print(f"\n1️⃣ Getting table structure:")
        try:
            structure = cortex_client.execute_query('DESCRIBE TABLE "dbo"."orders"')
            print(f"   📋 Found {len(structure)} columns")
            
            key_patterns = ['ID', 'CUSTOMER', 'DATE', 'STATUS', 'AMOUNT', 'TOTAL', 'CHARGE', 'COMPANY', 'BILL']
            business_columns = []
            
            for col in structure:
                col_name = col.get('name', 'Unknown')
                col_type = col.get('type', 'Unknown')
                
                is_business = any(pattern in col_name.upper() for pattern in key_patterns)
                if is_business:
                    business_columns.append((col_name, col_type))
                    print(f"   🎯 {col_name} ({col_type})")
                    
        except Exception as e:
            print(f"   ❌ Cannot describe table: {e}")
            return None
            
        print(f"\n2️⃣ Sample data to understand column content:")
        try:
            if business_columns:
                col_names = [col[0] for col in business_columns[:10]]  # First 10 business columns
                col_list = ', '.join([f'"{col}"' for col in col_names])
                sample_query = f'SELECT TOP 3 {col_list} FROM "dbo"."orders"'
            else:
                sample_query = 'SELECT TOP 3 * FROM "dbo"."orders"'
                
            sample = cortex_client.execute_query(sample_query)
            
            if sample:
                print(f"   📊 Sample record columns: {list(sample[0].keys())}")
                for i, record in enumerate(sample):
                    print(f"   📝 Record {i+1}:")
                    for key, value in list(record.items())[:5]:  # Show first 5 fields
                        print(f"      {key}: {value}")
            else:
                print("   ❌ No sample data found")
                
        except Exception as e:
            print(f"   ❌ Cannot get sample data: {e}")
            
        print(f"\n3️⃣ Recommended column mappings for business queries:")
        if business_columns:
            id_cols = [col for col, _ in business_columns if 'ID' in col.upper()]
            date_cols = [col for col, _ in business_columns if 'DATE' in col.upper()]
            customer_cols = [col for col, _ in business_columns if any(x in col.upper() for x in ['CUSTOMER', 'COMPANY', 'CLIENT'])]
            amount_cols = [col for col, _ in business_columns if any(x in col.upper() for x in ['AMOUNT', 'TOTAL', 'CHARGE', 'COST', 'PRICE'])]
            status_cols = [col for col, _ in business_columns if 'STATUS' in col.upper()]
            
            mappings = {
                'ID columns': id_cols[:3],
                'Date columns': date_cols[:3], 
                'Customer columns': customer_cols[:3],
                'Amount columns': amount_cols[:3],
                'Status columns': status_cols[:3]
            }
            
            for category, cols in mappings.items():
                if cols:
                    print(f"   💼 {category}: {', '.join(cols)}")
                    
            return mappings
        
        return None
        
    except Exception as e:
        print(f"❌ Inspection failed: {e}")
        return None

if __name__ == "__main__":
    mappings = inspect_orders_columns()
    if mappings:
        print(f"\n✅ Column inspection complete - update semantic queries with these column names")
    else:
        print(f"\n❌ Could not determine correct column names")
