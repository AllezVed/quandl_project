from db_utils import *
from utils import *
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
sns.set_style('darkgrid')


class Analyzer:
    def get_annual_vol(self, contract_root):
        """
        Calculate the annualized volatility of returns for each contract of this contract root.
        sort it by the annualized_vol DESC

        :param contract_root: specified contract root
        :return: df_annual_vol(DataFrame): Returns DataFrame of Annualized Volatility for each contract of specified
        contract root sorted in descending order
        """
        engine, query = generate_sql_query(contract_root)

        df = pd.read_sql(sql=query, con=engine)
        # df.to_csv('../csv_test.csv')
        df['returns'] = df.groupby(['name']).price.pct_change()

        ann_vol = df.groupby(['name']).agg({'returns': 'std'}) * np.sqrt(252)

        ann_vol.sort_values(by='returns', ascending=False)

        ann_vol.columns = ['annualized_vol']

        return ann_vol

    def get_trailing_1yr_vol(self, contract_root):
        """
        Calculates the trailing 1 year volatility of returns for each contract of this contract root.
        Rolling period used is 252 which is equivalent to the number of trading days in a year.
        :param contract_root: specified contract root
        :return: ans(DataFrame): Last data-point of trailing 1 year volatility for each contract of
        specified contract root sorted in descending order.
        """
        engine, query = generate_sql_query(contract_root)

        df = pd.read_sql(sql=query, con=engine)

        df['returns'] = df.groupby(['name']).price.pct_change()
        # using 252 as yearly count to be consistent with the number of trading days in a year
        trailing_1yr_vol = df.groupby(['name'])['returns'].rolling(252).std().reset_index()

        ans = trailing_1yr_vol.groupby(['name']).nth(-1)

        ans.drop(columns=['level_1'], inplace=True)
        ans.sort_values(by='returns', ascending=False, inplace=True)

        ans.columns = ['trailing_1yr_vol']

        return ans

    def get_largest_single_day_return(self, contract_root):
        """
        Calculates the largest single day return for each series of specified contract root and
        returns them sorted in descending order.
        :param contract_root: specified contract root
        :return: c_ans(DataFrame): largest single day returns of each series of contract root
        sorted in descending order.
        """

        engine, query = generate_sql_query(contract_root)

        df = pd.read_sql(sql=query, con=engine)

        df['returns'] = df.groupby(['name']).price.pct_change()

        max_idx = df.groupby('name')['returns'].idxmax()

        c_ans = df.loc[max_idx, ['name', 'date', 'returns']].reset_index(drop=1)

        c_ans.rename(columns={'returns': 'single_day_return'}, inplace=True)

        cols = list(c_ans.columns)
        cols = cols[1::2] + cols[::2]

        c_ans = c_ans[cols]

        c_ans.sort_values(by="single_day_return", ascending=False, inplace=True)

        return c_ans


    def get_largest_annual_return(self, contract_root):

        """
        Returns year of largest annual return for each contract in the specified contract root
        :param contract_root(str): specified contract root
        :return: df2 (DataFrame): largest annual return for each contract in descending order
        """

        engine, query = generate_sql_query(contract_root)

        df = pd.read_sql(sql=query, con=engine)

        df['returns'] = df.groupby(['name']).price.pct_change()


        df.date = df.date.apply(pd.to_datetime)

        annual_group = df.groupby(['name', df.date.dt.year]).agg({'returns': 'mean'})

        annual_group['annual_return'] = (np.power((annual_group['returns'] + 1), 252) - 1) * 100

        annual_group.drop(columns=['returns'], inplace=True)

        d_ans = annual_group[annual_group['annual_return'] == annual_group.groupby(level=[0])['annual_return'].transform(max)]


        df2 = d_ans.reset_index()

        df2.reset_index(drop=True, inplace=True)

        cols = list(df2.columns)
        cols = cols[::2] + cols[1::2]

        df2 = df2[cols]
        df2.sort_values(by='annual_return', ascending=False, inplace=True)
        df2['annual_return'] = df2['annual_return'].round(2).astype(str) + '%'

        return df2


    def get_sharpe_ratios(self, contract_root):
        """
        Returns the sharpe ratio for every commodity in the series
        :param contract_root:
        :return: sr_ans: Sharpe ratios for commodities of the contract root in descending order
        """

        engine, query = generate_sql_query(contract_root)

        df = pd.read_sql(sql=query, con=engine)

        df['returns'] = df.groupby(['name']).price.pct_change()

        sr_ans = df.groupby(['name']).agg({'returns': (np.mean, np.std)})

        sr_ans['sharpe_ratio'] = sr_ans[('returns', 'mean')].divide(sr_ans[('returns', 'std')]) * np.sqrt(252)

        sr_ans.drop(columns=[('returns', 'mean'), ('returns', 'std')], inplace=True)

        sr_ans.sort_values(by="sharpe_ratio", ascending=False, inplace=True)

        return sr_ans

    def chart_contracts(self, contract_type):
        """
        Charts every commodity of the specified contract_type in one plot and saves the image in ./images/
        :param contract_type: Specified contract root
        :return: None
        """

        engine, query = generate_sql_query(contract_type)

        df = pd.read_sql(sql=query, con=engine)

        df_pivot = df.pivot(index='date', columns='name', values='price')

        df_pivot.plot(figsize=(16, 9), title=f'Futures prices of {contract_type} for all contracts')

        plt.ylabel('Settle price($)')

        plt.savefig(f'./images/{contract_type}.png')


    def chart_contract(self, code_name):
        """
        Charts the series specified.
        :param code_name: series/contract name
        :return: None
        """

        engine, query = generate_sql_query(code_name, singular=True)

        df = pd.read_sql(sql=query, con=engine)

        df.plot(figsize=(16, 9), title=f'Futures prices of {code_name}')

        plt.ylabel('Settle price($)')

        plt.savefig(f'./images/{code_name}.png')






if __name__ == "__main__":

    analyzer = Analyzer()

    df_res = analyzer.get_sharpe_ratios("CME_GC")
    #
    print(df_res)
    #
    # df_largest_annual_return = analyzer.get_largest_annual_return("CME_NQ")
    #
    # print(df_largest_annual_return)
    #
    # df_trailing_1yr_vol = analyzer.get_trailing_1yr_vol("CME_CL")
    #
    # print(df_trailing_1yr_vol)
    #
    # df_annualized_vol = analyzer.get_annual_vol("CME_NG")
    #
    # print(df_annualized_vol)
    #
    # df_single_day = analyzer.get_largest_single_day_return("CME_GC")
    #
    # print(df_single_day)

    # analyzer.chart_contracts("CME_GC")

    # analyzer.chart_contract("CME_ES3")
