from sqlalchemy import create_engine, text

db_conn_string = 'mssql+pyodbc://@./E-CommerceDB?driver=ODBC+Driver+18+for+SQL+Server&trusted_connection=yes&Encrypt=no'

try:
    engine = create_engine(db_conn_string)
    with engine.connect() as conn:
        print('✓ Connected to database')
        
        # Insert data
        with open(r'Main Queries\SQLQuery = Insert Data Into Tables.sql', 'r') as f:
            insert_sql = f.read()
        
        insert_batches = insert_sql.split('GO')
        success_count = 0
        for batch in insert_batches:
            batch = batch.strip()
            if batch and not batch.startswith('--'):
                try:
                    conn.execute(text(batch))
                    success_count += 1
                except Exception as e:
                    err_str = str(e)
                    if 'Duplicate' in err_str or 'already exists' in err_str:
                        pass  # Data might already be inserted
                    else:
                        print(f'Note: {err_str[:100]}')
        
        conn.commit()
        print(f'✓ Data processing complete ({success_count} batches executed)')
        
except Exception as e:
    print(f'Error: {str(e)[:300]}')
