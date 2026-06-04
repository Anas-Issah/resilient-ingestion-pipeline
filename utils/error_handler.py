from logging.handlers import RotatingFileHandler
import logging


class FatalError(Exception):pass

class TransientErrorBackoff(Exception):pass

class AuthValidationError(Exception):pass

class TransientErrorRetry(Exception):pass

logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    "pipeline.log",
    maxBytes=4_000_000,
    backupCount=5

)
formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
handler.setFormatter(formatter)
handler.setLevel(logging.INFO)

def run_pipeline(func1,func2,func3,func4,func5,func6):
    def decorator(func):
        def wrapper(*args, **kwags):
            pipe_running = True
            while pipe_running:
                try:
                    retry = 3
                    back_of = 1
                    extracted_data = func1.extractor()
                    if not type(extracted_data) == list:
                        if 400 <= extracted_data and 500 > extracted_data:
                            if extracted_data == 429:
                                back_of *= 2
                                raise TransientErrorBackoff(f"{extracted_data}: Rate limit error.Implementing backoff retry.Backoff time {back_of} seconds")
                            elif extracted_data == 401 or extracted_data == 403:
                                raise AuthValidationError(f"{extracted_data}: Authentication or validation error encountered:Pipeline stopped")
                            else:
                                raise FatalError(f"{extracted_data}: Fatal network error occured.Pipeline stopped")
                        else:
                            if extracted_data == 503:
                                back_of *= 2
                                raise TransientErrorBackoff(f"{extracted_data}:backoff delay implemented")
                            else :
                                retry -= 1
                                raise TransientErrorRetry(f"{extracted_data}:Retrying connecting to source - retries left {retry}")
                    else:
                        # get coin ids and transform data to required format
                        stored_coin_ids = [coin["id"] for coin in extracted_data[0]]
                        transformed_data = func2.transform_data(stored_coin_ids, extracted_data)

                        #connect to database
                        db_connector = func3.db_connector()
                        if db_connector == 0:
                            raise FatalError(f"Programming or Interface error during database connection: Pipeline stopped!")

                        elif db_connector == 1:
                            retry-= 1
                            raise TransientErrorRetry(f"A transient error occured during database connection: retries left {retry}")
                        else:
                            # audit database
                            func4.coin_tb_auditor(coin_tb=extracted_data[1],engine=extracted_data[0])
                            func5.coin_details_tb_auditor(coin_details_tb=extracted_data[2],engine=extracted_data[0])
                            #load data
                            func6.loader(connector=extracted_data[:3],transformed_data=transformed_data)
                            #reset backoff and retries
                            back_of = 1
                            retry = 1
                except FatalError as e:
                    logger.exception(e,f"-{func.__name__}")
                    pipe_running = False
                except AuthValidationError as e:
                    logger.exception(e,f"-{func.__name__}")
                    pipe_running = False
                except TransientErrorBackoff as e:
                    logger.warning(e,f"-{func.__name__}")
                except TransientErrorRetry as e:
                    if (retry < 1):
                        pipe_running = False
                        logger.warning(e,f"-{func.__name__}-pipeline stopped.")
                    else:
                        logger.warning(e,f"-{func.__name__}")

