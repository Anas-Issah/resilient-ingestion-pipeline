
from pipelines import transform, extract, load
from config import database
from utils import auditor


from sqlalchemy import select

extracted_data = extract.extrator()
connector = database.db_connector()

#auditing
auditor.coin_tb_auditor(coin_tb=connector[1],engine=connector[0])
auditor.coin_details_tb_auditor(coin_details_tb=connector[2],engine=connector[0])


extracted_coin_id = connector[3]
transformed_data = transform.transform_data(extracted_coin_id,extracted_data)


load.loader(connector=connector[:3],transformed_data=transformed_data)
