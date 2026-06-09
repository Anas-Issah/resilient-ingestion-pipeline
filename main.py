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