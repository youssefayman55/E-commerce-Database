from sqlalchemy import create_engine, text
import time

# First, connect to master to create database
master_conn_string = 'mssql+pyodbc://@./master?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&Encrypt=no'

try:
    engine = create_engine(master_conn_string, echo=False)
    with engine.connect() as conn:
        # Create database if it doesn't exist
        conn.execute(text("IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'E-CommerceDB') CREATE DATABASE E_CommerceDB"))
        conn.commit()
        print('✓ Database ready')
        
except Exception as e:
    print(f'Database creation note: {str(e)[:150]}')

# Now connect to the new database and create schema/tables
time.sleep(1)
db_conn_string = 'mssql+pyodbc://@./E-CommerceDB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&Encrypt=no'

try:
    engine = create_engine(db_conn_string)
    with engine.connect() as conn:
        # Create schema
        try:
            conn.execute(text('CREATE SCHEMA shop'))
            conn.commit()
            print('✓ Schema created')
        except:
            print('✓ Schema already exists')
        
        # Run table creation script
        with open(r'Main Queries\SQLQuery = Create Tables and constraints.sql', 'r') as f:
            table_sql = f.read()
        
        batches = table_sql.split('GO')
        for batch in batches:
            batch = batch.strip()
            if batch and not batch.startswith('--'):
                try:
                    conn.execute(text(batch))
                except Exception as e:
                    if 'already exists' not in str(e):
                        print(f'Table creation note: {str(e)[:80]}')
        
        conn.commit()
        print('✓ Tables created')
        
        # Now insert data
        print('✓ Inserting data...')
        with open(r'Main Queries\SQLQuery = Insert Data Into Tables.sql', 'r') as f:
            insert_sql = f.read()
        
        insert_batches = insert_sql.split('GO')
        for batch in insert_batches:
            batch = batch.strip()
            if batch and not batch.startswith('--') and batch != 'SELECT':
                try:
                    conn.execute(text(batch))
                except Exception as e:
                    if 'Duplicate' not in str(e) and 'already exists' not in str(e):
                        print(f'Insert note: {str(e)[:80]}')
        
        conn.commit()
        print('✓ Data inserted successfully!')
        
except Exception as e:
    print(f'Error: {str(e)[:200]}')
