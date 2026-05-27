
def loader(connector:list,transformed_data):
    engine , coin_tb , coin_detaiils_tb = connector
    # load to coin_tb
    transformed_data[0].to_sql(coin_tb.name,engine,index=False,if_exists="append",method='multi')
    
    #load to coin_details_tb
    transformed_data[1].to_sql(coin_detaiils_tb.name,engine,index=False,if_exists="append",method="multi")

