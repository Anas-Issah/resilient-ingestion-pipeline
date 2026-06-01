import os
import time
from dotenv import load_dotenv
import requests
from pipelines import transform, extract, load
from config import database
from utils import auditor, error_handler

load_dotenv()

# retry = 3

# try:
#     extracted_data = extract.extrator()
#     if not type(extracted_data) == list:
#         if 400 <= extracted_data and 500 > extracted_data:
#             if extracted_data == 429:
#                 raise error_handler.TransientNetworkError(f"{extracted_data}: Rate limit error.Implementing backoff retry")
#             if extracted_data == 401 or extracted_data == 403:
#                 raise error_handler.AuthValidationError(f"{extracted_data}: Authentication or validation error encountered:Pipeline stopped")
#             else:
#                 raise error_handler.FatalNetworkError(f"{extracted_data}: Fatal network error occured.Pipeline stopped")
#         else:
#             if extracted_data == 503:
#                 raise error_handler.TransientNetworkError(f"{extracted_data}:backoff delay emplemented")
#             else :
#                 raise error_handler.TransientNetworkError(f"{extracted_data}:Retrying connecting to source")
            
#     else:
#         stored_coin_ids = [coin["id"] for coin in extracted_data[0]]
#         transformed_data = transform.transform_data(stored_coin_ids, extracted_data)
        
#         #connect to database
#         db_connector = database.db_connector()

# except error_handler.FatalNetworkError as e:
#     print(e)
# except error_handler.AuthValidationError as e:
#     print(e)



db = database.db_connector()
print(db)
# from sqlalchemy import select

# extracted_data = extract.extrator()
# print(extracted_data)
# connector = database.db_connector()

# #auditing
# auditor.coin_tb_auditor(coin_tb=connector[1],engine=connector[0])
# auditor.coin_details_tb_auditor(coin_details_tb=connector[2],engine=connector[0])


# extracted_coin_id = connector[3]
# transformed_data = transform.transform_data(extracted_coin_id,extracted_data)


# load.loader(connector=connector[:3],transformed_data=transformed_data)
