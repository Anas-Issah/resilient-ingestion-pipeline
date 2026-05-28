
from pipelines import transform, extract, load
from config import database


from sqlalchemy import select
# extracted_data = extract.extrator()
connector = database.db_connector()
# extracted_coin_id = connector[3]
# transformed_data = transform.transform_data(extracted_coin_id,extracted_data)
# 
# 
# load.loader(connector=connector[:3],transformed_data=transformed_data)
tb1 = connector[1]
from sqlalchemy import inspect
inpector = inspect(connector[0])
print([col['name'] for col in inpector.get_columns('coin_details_tb')])