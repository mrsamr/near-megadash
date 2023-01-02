import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title='On-Chain Activity - NEAR Mega Dashboard', 
    page_icon='📊',
    layout='wide'
)

@st.cache
def get_scorecard_data():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/b39ba359-ab65-4914-a205-59d26c27b449/data/latest'
    response = requests.get(url)
    raw_data = response.json()
    current_values = {
        m:{x['TIME_PERIOD']:x['CURRENT_VALUE'] for x in raw_data if x['METRIC']==m}
        for m in list(set([x['METRIC'] for x in raw_data]))
    }
    deltas = {
        m:{x['TIME_PERIOD']:x['DELTA'] for x in raw_data if x['METRIC']==m}
        for m in list(set([x['METRIC'] for x in raw_data]))
    }
    return current_values, deltas

@st.cache
def get_barchart_data():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/4ccaed65-867e-436c-a0ce-c0ee53176fe7/data/latest'
    response = requests.get(url)
    raw_data = response.json()
    barchart_data = pd.DataFrame(raw_data)
    barchart_data['UTC_DATE'] = pd.to_datetime(barchart_data['UTC_DATE'])
    barchart_data = barchart_data.rename(columns={'UTC_DATE':'Date',
                                                  'TRANSACTIONS':'Transactions',
                                                  'ACTIVE_ACCOUNTS':'Active Accounts',
                                                  'ACTIVE_CONTRACTS':'Active Contracts'})
    return barchart_data


scorecard_data, scorecard_deltas = get_scorecard_data()
barchart_data = get_barchart_data()


st.title('📊 On-Chain Activity')


st.write('')
with st.container():
    st.subheader('Transactions')
    
    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours', 
                      value='{:,}'.format(scorecard_data['Transactions']['P24H']), 
                      delta='{:.1%}'.format(scorecard_deltas['Transactions']['P24H']), 
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days', 
                      value='{:,}'.format(scorecard_data['Transactions']['P7D']), 
                      delta='{:.1%}'.format(scorecard_deltas['Transactions']['P7D']), 
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days', 
                      value='{:,}'.format(scorecard_data['Transactions']['P30D']), 
                      delta='{:.1%}'.format(scorecard_deltas['Transactions']['P30D']), 
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
            
    st.write('')
    st.area_chart(data=barchart_data, x='Date', y='Transactions',
                  use_container_width=True, height=500)


st.write('')
with st.container():
    st.subheader('Active Accounts')
    
    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours', 
                      value='{:,}'.format(scorecard_data['Active Accounts']['P24H']), 
                      delta='{:.1%}'.format(scorecard_deltas['Active Accounts']['P24H']), 
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days', 
                      value='{:,}'.format(scorecard_data['Active Accounts']['P7D']), 
                      delta='{:.1%}'.format(scorecard_deltas['Active Accounts']['P7D']), 
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days', 
                      value='{:,}'.format(scorecard_data['Active Accounts']['P30D']), 
                      delta='{:.1%}'.format(scorecard_deltas['Active Accounts']['P30D']),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
            
    st.write('')
    st.area_chart(data=barchart_data, x='Date', y='Active Accounts',
                  use_container_width=True, height=500)


st.write('')
with st.container():
    st.subheader('Active Contracts')
    
    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours', 
                      value='{:,}'.format(scorecard_data['Active Contracts']['P24H']), 
                      delta='{:.1%}'.format(scorecard_deltas['Active Contracts']['P24H']),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days', 
                      value='{:,}'.format(scorecard_data['Active Contracts']['P7D']), 
                      delta='{:.1%}'.format(scorecard_deltas['Active Contracts']['P7D']),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days', 
                      value='{:,}'.format(scorecard_data['Active Contracts']['P30D']), 
                      delta='{:.1%}'.format(scorecard_deltas['Active Contracts']['P30D']),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
            
    st.write('')
    st.area_chart(data=barchart_data, x='Date', y='Active Contracts',
                  use_container_width=True, height=500)
