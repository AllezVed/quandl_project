import quandl as qd
import pandas as pd
import config

from db_utils import *

qd.ApiConfig.api_key = config.api_key


class DataGetter:

    def get_contract(self, ctr_name):

        '''
        Gets the time series data from quandl for the specified contract
        :param: ctr_name(str):contract name/depth e.g., CME_ES1
        :return: contract (DataFrame): contract time-series data
        '''
        try:
            contract_data = qd.get(f'CHRIS/{ctr_name}')
        except Exception:
            print("Invalid API call. Check API key/your connection.")

        contract_data.reset_index(inplace=True)
        contract_data_cleaned = contract_data[['Date', 'Settle']]
        # contract_data_cleaned.set_index('Date', inplace=True)
        contract_data_cleaned.insert(0, 'name', ctr_name)
        contract_data_cleaned.rename(columns={'Date': 'date', 'Settle': 'price'}, inplace=True)
        return contract_data_cleaned





def get_contract_depth(ctr_root):
    '''
    Gets the futures depth for the specified contract root
    :param: ctr_root(str):contract name/depth e.g., CME_ES
    :return: contract (List): List of full contract names ['CME_ES1', 'CME_ES2', 'CME_ES3', 'CME_ES4']
    '''

    if 'NQ' in ctr_root:
        return [f'{ctr_root}{i}' for i in range(1, 3)]

    return [f'{ctr_root}{i}' for i in range(1, 5)]

    # def get_returns(self, ctr_df):














if __name__ == "__main__":
    dg = DataGetter()
    contract_roots = ['CME_ES', 'CME_NQ', 'CME_CL', 'CME_NG', 'CME_GC']
    contract_names = [root + str(i) for root in contract_roots for i in range(1, 5)]
    contract_names.remove('CME_NQ3')
    contract_names.remove('CME_NQ4')

    db_username = config.db_username
    db_password = config.db_password
    db_name = config.db_name

    db_object = DataBase(db_username, db_password, db_name)

    con, engine = db_object.create_and_connect_database()

    for name in contract_names:
        df = dg.get_contract(name)
        # df.to_csv(f'./data/{name}.csv')
        df.to_sql('contracts', con=engine, index=False, method='multi', if_exists='append')



















