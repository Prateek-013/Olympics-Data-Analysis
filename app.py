import streamlit as st
import pandas as pd
import preprocessor, Helper
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

df = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/Olympics-Data-Analysis/my-new-branch/athlete_events.csv')
region_df = pd.read_csv(r'https://raw.githubusercontent.com/Prateek-013/Olympics-Data-Analysis/my-new-branch/noc_regions.csv')



df = preprocessor.preprocess(df,region_df)

st.sidebar.title('Olympics Analysis')
st.sidebar.image(r'https://www.vectordiary.com/isd_tutorials/026-olympic-logos/torino/11.jpg')


user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)

if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, country = Helper.country_year_list(df)
    selected_year = st.sidebar.selectbox('Select Year', years)
    selected_country = st.sidebar.selectbox('Select Country', country)
    tally = Helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_country == 'All Countries' and selected_year == 'Overall':
        st.title("Overall Tally")
    if selected_country == 'All Countries' and selected_year != 'Overall':
        st.title('Medal Tally in' + str(selected_year) + 'Olympics')
    if selected_country != 'All Countries' and selected_year == 'Overall':
        st.title(str(selected_country) + ' Overall Performance')
    if selected_country != 'All Countries' and selected_year != 'Overall':
        st.title(str(selected_country) +"'s" + ' Performance in ' + str(selected_year) + ' Olympics')
    st.table(tally)

if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title('Top Statistics')

    col1,col2,col3 = st.columns(3)

    with col1:
        st.header('Editions')
        st.title(editions)
    with col2:
        st.header('Hosts')
        st.title(cities)
    with col3:
        st.header('Sports')
        st.title(sports)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Events')
        st.title(events)
    with col2:
        st.header('Athletes')
        st.title(athletes)
    with col3:
        st.header('Nations')
        st.title(nations)

    nations_over_time = Helper.dataovertime(df, 'region')
    fig = px.line(nations_over_time, x='Editions', y='Number of Countries')
    st.title('Participating Nations over the Years')
    st.plotly_chart(fig)

    events_over_time = Helper.dataovertime(df, 'Event')
    fig = px.line(events_over_time, x='Editions', y='Number of Events')
    st.title('Events over the Years')
    st.plotly_chart(fig)

    athlete_over_time = Helper.dataovertime(df, 'Name')

    fig = px.line(athlete_over_time, x='Editions', y='Number of Athletes')
    st.title('Number of Athletes over the Years')
    st.plotly_chart(fig)

    st.title("Number of Events over Time (By Every Sport)")
    fig, ax= plt.subplots(figsize=(25,25))
    x = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
    sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype(int),
                annot=True)
    st.pyplot(fig)

    st.title('Most Successful Athletes')
    sportlist = df['Sport'].unique().tolist()
    sportlist.sort()
    sportlist.insert(0, 'Overall')
    selected_sport = st.selectbox('Select a Sport', sportlist)
    x = Helper.mostsuccessful(df, selected_sport)
    st.table(x)

if user_menu == 'Country Wise Analysis':

    st.sidebar.title('Country Wise Analysis')
    regionlist = df['region'].dropna().unique().tolist()
    regionlist.sort()
    selected_country = st.sidebar.selectbox('Select a Country', regionlist)
    countrydf = Helper.yearwise_medal_tally(df, selected_country)
    fig = px.line(countrydf, x='Year', y='Medal')
    st.header(selected_country + ' Medal Tally over the Years')
    st.plotly_chart(fig)

    st.header(selected_country + ' excels in the following sports')
    pt = Helper.country_event_heatmap(df, selected_country)
    fig, ax = plt.subplots(figsize=(25, 25))
    x = df.drop_duplicates(subset=['Year', 'Sport', 'Event'])
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.header('Top 10 Most Successful Athletes of ' + selected_country)
    top10_df = Helper.mostsuccessful_by_country(df, selected_country)
    st.table(top10_df.head(10))

if user_menu == 'Athlete Wise Analysis':
    athletedf = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athletedf['Age'].dropna()
    x2 = athletedf[athletedf['Medal'] == 'Gold']['Age'].dropna()
    x3 = athletedf[athletedf['Medal'] == 'Silver']['Age'].dropna()
    x4 = athletedf[athletedf['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4],
                             ['Overall Age', 'Gold Medallist', 'Silver Medallist', 'Bronze Medallist'], show_hist=False,
                             show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header('Age Distribution of Athletes')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Athletics','Swimming','Rowing','Gymnastics', 'Fencing', 'Hockey',
     'Football', 'Sailing','Cycling','Wrestling','Shooting','Canoeing','Basketball', 'Water Polo', 'Handball',
     'Equestrianism','Volleyball','Boxing','Weightlifting','Diving','Judo','Archery','Baseball',
     'Tennis','Synchronized Swimming','Rugby','Modern Pentathlon','Softball','Badminton','Table Tennis',
     'Art Competitions','Rhythmic Gymnastics','Tug-Of-War','Taekwondo','Rugby Sevens']

    for sport in famous_sports:
        temp_df = athletedf[athletedf['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.header('Age Distribution of Gold Medallists by Sport')
    st.plotly_chart(fig)

    st.header('Height and Weight Comparison of Athletes')
    sportlist = df['Sport'].unique().tolist()
    sportlist.sort()
    selected_sport = st.selectbox('Select a Sport', sportlist)
    tempdf = Helper.weight_v_height(df,selected_sport)
    fig, ax = plt.subplots()
    ax = sns.scatterplot(data = tempdf,x = tempdf['Weight'], y=tempdf['Height'], style=tempdf['Sex'], hue=tempdf['Medal'], s=60)
    st.pyplot(fig)

    st.header('Men and Women Participation Over the Years')
    final = Helper.men_v_women(df)
    fig = px.line(final, x='Year', y=['Male', 'Female'])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)
