from sqlalchemy import engine,MetaData,URL,create_engine,inspect,Table,text
from dotenv import load_dotenv
import os

coin_tb_name = "coin_tb"
coin_details_tb_name = "coin_details_tb"

url = URL.create(
    "postgresql+psycopg2",
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME")
)

meta = MetaData()
engine = create_engine(url=url,pool_size=5,pool_timeout=5,pool_recycle=300,pool_pre_ping=True)

coin_tb_cols = ['id','name']
coin_details_tb_cols = [
                        'current_price', 'high_24h', 'low_24h', 'market_cap',
                        'total_volume', 'coin_id', 'last_updated'
                        ]
inspector = inspect(engine)
tables = inspector.get_table_names()
coin_tb = Table(coin_details_tb_name,meta,autoload_with=engine)
col = inspector.get_columns(coin_tb.name)
print(inspector.get_columns(coin_tb.name))

def coin_tb_auditor(coin_tb, engine):
    table_cols = [{"name":'id','type':"VARCHAR(length=10)"},
                  {"name":'name',"type":'VARCHAR(length=50)'}]
    inspector = inspect(engine)
    cols = inspector.get_columns(coin_tb.name)
    for col in table_cols:
        if col["name"] not in [c["name"] for c in cols]:
            col_type = "VARCHAR(10)" if col['type'].endswith("10)") else "VARCHAR(50)"
            add_column(coin_tb,engine,col["name"], col_type)
            
def coin_details_tb_auditor(coin_tb, engine):
    table_cols = [
                {"name":'current_price','type':"NUMERIC(precision=18,scale=2)"},{"name":'high_24h',"type":'NUMERIC(precision=18,scale=2)'},
                  {"name":'low_24h',"type":'NUMERIC(precision=18,scale=2)'},{"name":'market_cap',"type":'NUMERIC(precision=18,scale=2)'},
                  {"name":'total_volume',"type":'NUMERIC(precision=20,scale=2)'},{"name":'coin_id',"type":'VARCHAR(10)'},
                  {"name":'last_updated',"type":'TIMESTAMP(timezone=True)'}
                  ]
    inspector = inspect(engine)
    cols = inspector.get_columns(coin_tb.name)
    for col in table_cols:
        if col["name"] not in [c["name"] for c in cols]:
            if col["name"] == 'coin_id':
                col_type = 'VARCHAR(10)'
            elif(col["name"] == 'total_volume'):
                col_type = "NUMERIC(20,2)" 
            elif(col['name']=='last_updated'):
                col_type = "TIMESTAMPTZ"
            else:
                col_type = "NUMERIC(18,2)"
            add_column(coin_tb,engine,col["name"], col_type)

        
def add_column(table,engine,col_name,col_type):
    with engine.connect() as conn:
        conn.execute(text(f"ALTER TABLE {table.name} ADD COLUMN {col_name} {col_type}"))
        conn.commit()

