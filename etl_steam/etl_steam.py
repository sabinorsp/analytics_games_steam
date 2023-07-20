import time
import numpy as np
from tqdm import tqdm
from etl_configs import EtlSteam
from sqlalchemy import create_engine


def get_group_data(start:int) -> str:
    """
    Create the end point with parameter "start" to set the list item games to get.

    Args: 
        start (int): number of interval to get the list itens game, change in multiple 
                    of 50. 
    Return: 
        str: a string with the full link to get data about list games.
    """
    url = "https://store.steampowered.com/search/results/?query&start="+str(start*50)+\
       "&count=50&dynamic_data=&sort_by=_ASC&supportedlang=english&snr=1_7_7_230_7&infinite=1"
    return url


def save_data_DB(obj: object,schema_name:str, first_commit: bool) -> None:
    """
    Convert the dataframes to tables in a Postgres database using the SQLAlchemy engine.

    Args:
        obj (object): Instance of class EtlSteam() with executed method .getsummary_data() 
        first_commit (bool): boolean value: True to mode 'replace' and False to mode 'append'
        schema_name (str): Schame of DB name.
    """
    mode = 'replace' if first_commit == True else 'append'
    obj.data_info.to_sql(name ='info', con=engine, schema=schema_name ,if_exists=mode, index=True)
    obj.data_prices.to_sql(name='prices', con=engine, schema=schema_name, if_exists=mode, index=True)
    obj.data_links.to_sql(name='links', con=engine, schema=schema_name, if_exists=mode, index=True )
    obj.data_reviews.to_sql(name='reviews', con=engine,schema=schema_name, if_exists=mode, index=True)
    return None


def scroll_all_games(total_groups: int, schema_name: str) -> str:
    """
    Scroll about all list games present in site steam. 
    Execute the ETL process and save by block of 50 games in database

    Args:
        total_groups (int): total_games_on_steam/ 50
    
    Return: 
        string: mensage about finish process.
    """
    for group in tqdm(range(total_groups)):
        etl_steam = EtlSteam(get_group_data(group))
        etl_steam.get_summary_data()
        if group == 0: 
            save_data_DB(etl_steam,schema_name, True)
        else:
            save_data_DB(etl_steam,schema_name,False)
        time.sleep(np.random.random())
    return 'Finish ETL!'


# Connect to Postgres DB:
database = 'etl-steam'
user = 'docker' 
password = 'docker'
host = 'localhost'
engine = create_engine('postgresql+psycopg2://'+user+':'+password+'@'+host+'/'+database)

# Create instance to get total game present on steam page. 
obj = EtlSteam(get_group_data(0))
obj.get_summary_data()
obj.total_counts
total_groups = obj.total_counts//50

# Execute the ETL process.
scroll_all_games(total_groups,'public')
