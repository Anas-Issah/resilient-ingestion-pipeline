import os
import time
import requests
from ratelimit import limits, sleep_and_retry
from pipelines import transform, extract, load
from config import database
from utils import auditor, error_handler




config_decorator = error_handler.run_pipeline(transform,database,auditor,load)
limiter = limits(calls=30,period=60)
decorated_pipeline = config_decorator(extract.extrator)
fully_decorated_pipeline = sleep_and_retry(limiter(decorated_pipeline))
if __name__ == "__main__":
    fully_decorated_pipeline()

#     extracted_data = extract.extrator()
#     if not type(extracted_data) == list:
#         if 400 <= extracted_data and 500 > extracted_data:
#             if extracted_data == 429:
#                 raise error_handler.TransientError(f"{extracted_data}: Rate limit error.Implementing backoff retry")
#             if extracted_data == 401 or extracted_data == 403:
#                 raise error_handler.AuthValidationError(f"{extracted_data}: Authentication or validation error encountered:Pipeline stopped")
#             else:
#                 raise error_handler.FatalError(f"{extracted_data}: Fatal network error occured.Pipeline stopped")
#         else:
#             if extracted_data == 503:
#                 raise error_handler.TransientError(f"{extracted_data}:backoff delay emplemented")
#             else :
#                 raise error_handler.TransientError(f"{extracted_data}:Retrying connecting to source - retries left {retry}")
#             # 
#     else:
#         stored_coin_ids = [coin["id"] for coin in extracted_data[0]]
#         transformed_data = transform.transform_data(stored_coin_ids, extracted_data)
#         # 
#         #connect to database
#         db_connector = database.db_connector()
#         if db_connector == 0:
#             raise error_handler.FatalError(f"Programming or Interface error during database connection: Pipeline stopped!")
#         elif db_connector == 1:
#             retry-= 1
#             raise error_handler.TransientError(f"A transient error occured during database connection: retries left {retry}")
#         else:
#             # audit database
#             auditor.coin_tb_auditor(coin_tb=extracted_data[1],engine=extracted_data[0])
#             auditor.coin_details_tb_auditor(coin_details_tb=extracted_data[2],engine=extracted_data[0])
#             load.loader(connector=extracted_data[:3],transformed_data=transformed_data)
# # 
# except error_handler.FatalError as e:
#     print(e)
# except error_handler.AuthValidationError as e:
#     print(e)
# # 


# db = database.db_connector()
# print(db)
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
