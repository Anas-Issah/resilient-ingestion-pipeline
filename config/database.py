from sqlalchemy import MetaData, URL,Table,inspect,create_engine,select,text
from dotenv import load_dotenv
import os
load_dotenv(override=True)
def db_connector():
    url = URL.create(
        "postgresql+psycopg2",
        username=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME")
    )

    meta = MetaData()
    engine = create_engine(url=url,pool_size=5,pool_timeout=5,pool_recycle=300,pool_pre_ping=True)
    with engine.connect() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXIST coin_tb (" \
        "id VARCHAR(10) PRIMARY KEY NOT NULL,name VARCHAR(50)) NOT NULL"))

        conn.execute(text("CREATE TABLE IF NOT EXIST coin_detail_tb(" \
        "current_price NUMERIC(18,2) NOT NULL,high_24h NUMERIC(18,2) NOT NULL," \
        "low_24h NUMERIC(18,2) NOT NULL,market_cap NUMERIC(18,2) NOT NULL, total_volume NUMERIC(20,2) NOT NULL ," \
        " last_updated TIMESTAMPTZ NOT NULL"))
        
    coin_tb = Table("coin_tb",meta,autoload_with=engine)
    coin_detail_tb = Table("coin_detail_tb",meta,autoload_with=engine)
    return [engine, coin_tb, coin_detail_tb ]
