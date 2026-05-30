from sqlalchemy import inspect, text

def coin_tb_auditor(coin_tb, engine):
    table_cols = [{"name":'id','type':"VARCHAR(10)"},
                  {"name":'name',"type":'VARCHAR(50)'}]
    inspector = inspect(engine)
    cols = inspector.get_columns(coin_tb.name)
    col_names = [c["name"] for c in cols]
    col_names_types = [[c["name"],c["type"]] for c in cols]

    for col in table_cols:
        if col["name"] not in col_names:
            col_type = col["type"]
            add_column(coin_tb,engine,col["name"], col_type)

        elif [col["name"],col["type"]] not in col_names_types:
            col_type = col["type"]
            alter_column_coin(coin_tb,engine,col["name"],col_type)

            
def coin_details_tb_auditor(coin_details_tb, engine):
    table_cols = [
                {"name":'current_price','type':"NUMERIC(18, 2)"},{"name":'high_24h',"type":'NUMERIC(18, 2)'},
                  {"name":'low_24h',"type":'NUMERIC(18, 2)'},{"name":'market_cap',"type":'NUMERIC(18, 2)'},
                  {"name":'total_volume',"type":'NUMERIC(20, 2)'},{"name":'coin_id',"type":'VARCHAR(10)'},
                  {"name":'last_updated',"type":'TIMESTAMP'}
                  ]
    inspector = inspect(engine)
    cols = inspector.get_columns(coin_details_tb.name)
    col_names = [c["name"] for c in cols]
    col_names_types = [[str(c["name"]),str(c["type"])] for c in cols]
   
   
    for col in table_cols:
        if col["name"] not in col_names: 
            if col["name"] == 'coin_id':
                col_type = 'VARCHAR(10)'
            elif(col["name"] == 'total_volume'):
                col_type = "NUMERIC(20,2)" 
            elif(col['name']=='last_updated'):
                col_type = "TIMESTAMPTZ"
            else:
                col_type = "NUMERIC(18,2)"
            add_column(table=coin_details_tb,engine=engine,col_name=col["name"],col_type= col_type)

        elif [col["name"],col["type"]] not in col_names_types:
            col_type = "TIMESTAMPTZ" if col["type"] == "TIMESTAMP" else col["type"] if col["type"] == "VARCHAR(10)" else "NUMERIC(20, 2)"
            alter_column_coin_details(table=coin_details_tb,engine=engine,col_name=col["name"],col_type=col_type)
            
    

def add_column(table,engine,col_name,col_type):
    with engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table.name} ADD COLUMN {col_name} {col_type}"))
        conn.commit()

def alter_column_coin(table,engine,col_name,col_type):
    
    query = text(f"""ALTER TABLE {table.name} 
                     ALTER COLUMN {col_name} TYPE {col_type} USING {col_name}::varchar""")
    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()

def alter_column_coin_details(table,engine,col_name,col_type):
    if col_type == "NUMERIC(20, 2)":
        query = text(f"""ALTER TABLE {table.name} 
                     ALTER COLUMN {col_name} TYPE {col_type} USING {col_name}::numeric""")
    elif col_type == "VARCHAR(10)":
            query = text(f"""ALTER TABLE {table.name} 
                     ALTER COLUMN {col_name} TYPE {col_type} USING {col_name}::varchar""")
    elif col_type == "TIMESTAMPTZ":
        query = text(f"""ALTER TABLE {table.name} 
                     ALTER COLUMN {col_name} TYPE {col_type} USING {col_name}::timestamptz""")
    with engine.connect() as conn:
        conn.execute(query)
        conn.commit()
