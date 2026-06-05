from functools import wraps
from logging.handlers import RotatingFileHandler
import logging
import time


class FatalError(Exception):pass

class TransientErrorBackoff(Exception):pass

class AuthValidationError(Exception):pass

class TransientErrorRetry(Exception):pass

class NetworkConnectionError(Exception):pass

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
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
logger.addHandler(handler)


def run_pipeline(m1,m2,m3,m4):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwags):
            pipe_running = True
            retry = 3
            back_of = 1
            while pipe_running:
                try:
                    extracted_data = func()
                    if not type(extracted_data) == list:
                        if extracted_data == 1:
                            back_of *= 2
                            retry -= 1
                            raise NetworkConnectionError(f"{extracted_data}:Connection or Timeout error occured-retry in {back_of} second-"
                                                         f"retries left {retry}")
                        elif 400 <= extracted_data and 500 > extracted_data:
                            if extracted_data == 429:
                                back_of *= 2
                                raise TransientErrorBackoff(f"{extracted_data}: Rate limit error.Implementing backoff retry."
                                                            f"Backoff time {back_of} seconds-[{func.__qualname__}]")
                            elif extracted_data == 401 or extracted_data == 403:
                                raise AuthValidationError(f"{extracted_data}: Authentication or validation error encountered:Pipeline stopped")
                            else:
                                raise FatalError(f"{extracted_data}: Fatal network error occured.Pipeline stopped-[{func.__qualname__}]")
                        else:
                            if extracted_data == 503:
                                back_of *= 2
                                raise TransientErrorBackoff(f"{extracted_data}:backoff delay implemented-[{func.__qualname__}]")
                            else :
                                retry -= 1
                                raise TransientErrorRetry(f"{extracted_data}:Retrying connecting to source -" 
                                                          f"retries left {retry}-[{func.__qualname__}]")
                    else:
                        #connect to database
                        db_connector = m2.db_connector()
                        if db_connector == 0:
                            raise FatalError(f"Programming or Interface error during database connection:" 
                                             f"Pipeline stopped!-[{m2.db_connector.__qualname__}]")

                        elif db_connector == 1:
                            retry-= 1
                            raise TransientErrorRetry(f"A transient error occured during database connection:" 
                                                      f"retries left {retry}-[{m2.db_connector.__qualname__}]")
                        else:
                              # get coin ids and transform data to required format
                            stored_coin_ids = db_connector[3]
                            transformed_data = m1.transform_data(stored_coin_ids, extracted_data)
                            # audit database
                            m3.coin_tb_auditor(coin_tb=db_connector[1],engine=db_connector[0])
                            m3.coin_details_tb_auditor(coin_details_tb=db_connector[2],engine=db_connector[0])
                            #load data
                            m4.loader(connector=db_connector[:3],transformed_data=transformed_data)
                            #reset backoff and retries
                            back_of = 1
                            retry = 3
                except FatalError as e:
                    logger.exception(e)
                    pipe_running = False
                except AuthValidationError as e:
                    logger.exception(e)
                    pipe_running = False
                except TransientErrorBackoff as e:
                    logger.warning(e)
                    time.sleep(back_of)
                except TransientErrorRetry as e:
                    if (retry < 1):
                        pipe_running = False
                        logger.warning(e,"-Pipeline stopped.")
                    else:
                        logger.warning(e)
                except NetworkConnectionError as e:
                    if (retry < 1):
                        pipe_running = False
                        logger.warning(f"{e} -Pipeline stopped.")
                    else:
                        logger.warning(e)
                        time.sleep(back_of)
        return wrapper
    return decorator

