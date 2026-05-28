import pandas as pd


def transform_data(stored_coin_ids:list,data:list):
    """
    transforms the clean extracted data into a pandas dataframe
    """
    # coin_tb
    coin_tb = pd.DataFrame(data[0])
    coin_tb = coin_tb[~coin_tb["id"].isin(stored_coin_ids)]
    coin_tb.dropna(inplace=True)

    # coin_details_df
    coin_details_df = pd.DataFrame(data[1])
    coin_details_df["last_updated"] = pd.to_datetime(coin_details_df["last_updated"])
    coin_details_df.dropna(inplace=True)
    return [coin_tb,coin_details_df]
