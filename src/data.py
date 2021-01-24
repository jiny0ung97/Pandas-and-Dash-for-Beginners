import pandas as pd

def make_country_df(country='global'):
    def make_df(condition):
        df = pd.read_csv(f'../data/time_series_{condition}.csv')
        if country != 'global':
            df = df.loc[df['Country/Region'] == country]
            
        df = df.drop(['Province/State', 'Country/Region', 'Lat', 'Long'], axis=1).sum().reset_index(name=condition)
        df = df.rename(columns={'index': 'date'})
        return df

    conditions = ['confirmed', 'deaths', 'recovered']
    final_df = None

    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df

daily_df = pd.read_csv('../data/daily_reports.csv')
totals_df = daily_df[['Confirmed', 'Deaths', 'Recovered']].sum().reset_index(name='count')
totals_df = totals_df.rename(columns={'index': 'condition'})

countries_df = daily_df[['Country_Region', 'Confirmed', 'Deaths', 'Recovered']]
countries_df = countries_df.groupby('Country_Region').sum().reset_index()