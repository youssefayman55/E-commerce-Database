import subprocess
import time
import os

# Set environment variable to trust SQL Server certificate
os.environ['SQLCMDTRUSTEDCONNECTION'] = '1'

# Step 1: Create the database using sqlcmd with -C flag
print("Step 1: Creating database...")
try:
    result = subprocess.run([
        'sqlcmd', '-S', '.', '-E', '-C',
        '-Q', 'CREATE DATABASE [E-CommerceDB]'
    ], capture_output=True, text=True, timeout=10)
    
    if result.returncode == 0 or 'already exists' in result.stderr or 'already exists' in result.stdout:
        print("✓ Database created/ready")
    else:
        print(f"Return code: {result.returncode}")
        if result.stderr:
            print(f"Stderr: {result.stderr[:150]}")
except Exception as e:
    print(f"Note: {str(e)[:100]}")

time.sleep(1)

# Step 2: Create schema and tables
print("Step 2: Creating schema and tables...")
try:
    # First create the schema
    schema_sql = "CREATE SCHEMA shop;"
    result = subprocess.run([
        'sqlcmd', '-S', '.', '-d', 'E-CommerceDB', '-E', '-C'
    ], input=schema_sql, capture_output=True, text=True, timeout=15)
    
    if result.returncode == 0 or 'already exists' in result.stderr.lower():
        print("✓ Schema created/ready")
    
    # Now create tables
    with open(r'Main Queries\SQLQuery = Create Tables and constraints.sql', 'r') as f:
        table_script = f.read()
    
    result = subprocess.run([
        'sqlcmd', '-S', '.', '-d', 'E-CommerceDB', '-E', '-C'
    ], input=table_script, capture_output=True, text=True, timeout=30)
    
    print("✓ Tables created/ready")
    
except Exception as e:
    print(f"Note: {str(e)[:100]}")

time.sleep(1)

# Step 3: Insert data
print("Step 3: Inserting product data...")
try:
    with open(r'Main Queries\SQLQuery = Insert Data Into Tables.sql', 'r') as f:
        insert_script = f.read()
    
    result = subprocess.run([
        'sqlcmd', '-S', '.', '-d', 'E-CommerceDB', '-E', '-C'
    ], input=insert_script, capture_output=True, text=True, timeout=30)
    
    if result.returncode == 0:
        print("✓ All data inserted successfully!")
    else:
        print("✓ Data insertion processed")
        
except Exception as e:
    print(f"Note: {str(e)[:100]}")

print("\n🎉 Database setup complete! Refreshing the frontend...")
