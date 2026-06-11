import os,requests
from dotenv import load_dotenv
load_dotenv()


def extrator():
    key = "ke" #os.getenv("CG_key")
    headers ={
        "accept":"application/json",
        "x_cg_demo_api_key":key

    }
    params = {
        "_page":1,
        "per_page":20,
        "vs_currency":'usd',
        "order":"market_cap_rank_asc"
    }
    url = str(os.getenv("CG_URL"))
    try:
    
        response = requests.get(url=url,headers=headers,params=params)
        if response.ok:
            return [

                        [{"id":coin["symbol"],"name":coin["name"]}  for coin in response.json()],
                        [   {"current_price":coin["current_price"],"market_cap":coin["market_cap"],
                            'high_24h':coin["high_24h"],"low_24h":coin["low_24h"], "total_volume":coin["total_volume"],
                            "coin_id":coin["symbol"],'last_updated':coin["last_updated"]}
                            for coin in response.json()]
                    ]
        else:
            return response.status_code
        
    except (requests.exceptions.ConnectionError,requests.exceptions.Timeout):
        return 1
    
    