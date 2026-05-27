
from pipelines import transform, extract, load
from config import database


from sqlalchemy import select
extracted_data = extract.extrator()
extracted_coin_id = [coin["id"] for coin in extracted_data[0]]
transformed_data = transform.transform_data(extracted_coin_id,extracted_data)
connector = database.db_connector()

load.loader(connector=connector,transformed_data=transformed_data)