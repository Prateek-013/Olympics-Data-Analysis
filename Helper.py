import pandas as pd
import numpy as np

def medal_tally(df):
    tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                               keep='first').groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
    tally['Total'] = tally['Gold'] + tally['Silver'] + tally['Bronze']
    tally['Rank'] = tally['Total'].rank(ascending=False, method='min').astype('int')
    tally.reset_index(inplace=True)
    tally = tally[['Rank', 'region', 'Gold', 'Silver', 'Bronze', 'Total']]
    tally.set_index('Rank', inplace=True)
    tally.sort_values('Total', ascending=False, inplace=True)
    return tally


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = df['region'].dropna().unique().tolist()
    country.sort()
    country.insert(0, 'All Countries')

    return years, country


def fetch_medal_tally(df, year, country):
    newdf = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'],
                               keep='first')
    flag = 0
    if year == 'Overall' and country == 'All Countries':
        temp_df = newdf

    if year == 'Overall' and country != 'All Countries':
        flag = 1
        temp_df = newdf[newdf['region'] == country]

    if year != 'Overall' and country == 'All Countries':
        temp_df = newdf[newdf['Year'] == int(year)]

    if year != 'Overall' and country != 'All Countries':
        temp_df = newdf[(newdf['Year'] == int(year)) & (newdf['region'] == country)]

    if flag == 0:
        x = temp_df.groupby('region')[['Gold', 'Silver', 'Bronze']].sum()
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
        x = x.sort_values('Total', ascending=False).reset_index()
    if flag == 1:
        x = temp_df.groupby('Year')[['Gold', 'Silver', 'Bronze']].sum().sort_values('Year').reset_index()
        x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    return x

def dataovertime(df, col):
    nationsovertime = df.drop_duplicates(subset=['Year', col], keep='first')[
        'Year'].value_counts().reset_index().sort_values('index')
    nationsovertime.rename(columns={"index": "Editions", 'Year': col}, inplace=True)

    if nationsovertime.columns.tolist()[1] == 'Name':
        nationsovertime.rename(columns={col: 'Number of Athletes'}, inplace=True)

    if nationsovertime.columns.tolist()[1] == 'Event':
        nationsovertime.rename(columns={col: 'Number of Events'}, inplace=True)

    if nationsovertime.columns.tolist()[1] == 'region':
        nationsovertime.rename(columns={col: 'Number of Countries'}, inplace=True)

    return nationsovertime


def mostsuccessful(df, sport):
    tempdf = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        tempdf = tempdf[tempdf['Sport'] == sport]

    x = tempdf['Name'].value_counts().reset_index().merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x.head(25)

def yearwise_medal_tally(df, country):
    tempdf = df.dropna(subset=['Medal'])
    tempdf.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    finaldf = tempdf[tempdf['region'] == country].groupby('Year').count()['Medal'].reset_index()
    return finaldf

def country_event_heatmap(df, country):
    tempdf = df.dropna(subset=['Medal'])
    tempdf.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Season', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    newdf = tempdf[tempdf['region'] == 'USA']
    pt = newdf.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt


def mostsuccessful_by_country(df, country):
    tempdf = df.dropna(subset=['Medal'])

    tempdf = tempdf[tempdf['region'] == country]

    x = tempdf['Name'].value_counts().reset_index().merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport']].drop_duplicates('index')

    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def weight_v_height(df, sport):

    athletedf = df.drop_duplicates(subset=['Name', 'region'])
    athletedf["Medal"].fillna('No Medal', inplace=True)
    tempdf = athletedf[athletedf['Sport'] == 'Athletics']
    return tempdf

def men_v_women(df):
    athletedf = df.drop_duplicates(subset=['Name', 'region'])
    men = athletedf[athletedf['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athletedf[athletedf['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = men.merge(women, on='Year', how='left')
    final.fillna(0, inplace=True)
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    return final