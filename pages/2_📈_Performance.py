import streamlit as st
import pandas as pd
import requests

st.set_page_config(
    page_title='Performance - NEAR Mega Dashboard', 
    page_icon='📈',
    layout='wide'
)

def render_safe(value, format):
    try:
        x = format.format(value)
    except:
        x = None
    return x

@st.cache
def get_scorecard_data():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/3b9a57ee-b1a9-4a59-b3f9-8583e186669c/data/latest'
    response = requests.get(url)
    data = response.json()
    return data[0]

@st.cache
def get_barchart_data():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/4922bf59-2feb-4b45-be10-fc316d11520e/data/latest'
    response = requests.get(url)
    raw_data = response.json()
    barchart_data = pd.DataFrame(raw_data)
    barchart_data['UTC_DATE'] = pd.to_datetime(barchart_data['UTC_DATE'])
    return barchart_data


scorecard_data = get_scorecard_data()
barchart_data = get_barchart_data()


st.title('📈 Blockchain Performance')

st.write('')
with st.container():
    st.subheader('Blocks Produced')
    
    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours', 
                      value=render_safe(scorecard_data['BLOCKS_PRODUCED__PAST_24H'],  '{:,}'),
                      delta=render_safe(scorecard_data['BLOCKS_PRODUCED__DELTA_24H'], '{:.1%}'),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days', 
                      value=render_safe(scorecard_data['BLOCKS_PRODUCED__PAST_7D'],  '{:,}'),
                      delta=render_safe(scorecard_data['BLOCKS_PRODUCED__DELTA_7D'], '{:.1%}'),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days', 
                      value=render_safe(scorecard_data['BLOCKS_PRODUCED__PAST_30D'],  '{:,}'),
                      delta=render_safe(scorecard_data['BLOCKS_PRODUCED__DELTA_30D'], '{:.1%}'),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

    chart_data = barchart_data[['UTC_DATE','BLOCKS_PRODUCED']]
    chart_data = chart_data.rename(columns={'UTC_DATE':'Date', 'BLOCKS_PRODUCED':'Blocks'})
    st.write()
    st.area_chart(data=chart_data, x='Date', y='Blocks',
                  use_container_width=True, height=500)


st.write('')
with st.container():
    st.subheader('Block Time')

    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours (Avg)', 
                      value=render_safe(scorecard_data['BLOCK_TIME_SECONDS__PAST_24H'],  '{:.2}s'),
                      delta=render_safe(scorecard_data['BLOCK_TIME_SECONDS__DELTA_24H'], '{:.1%}'),
                      delta_color="inverse", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days (Avg)', 
                      value=render_safe(scorecard_data['BLOCK_TIME_SECONDS__PAST_7D'],  '{:.2}s'),
                      delta=render_safe(scorecard_data['BLOCK_TIME_SECONDS__DELTA_7D'], '{:.1%}'),
                      delta_color="inverse", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days (Avg)', 
                      value=render_safe(scorecard_data['BLOCK_TIME_SECONDS__PAST_30D'],  '{:.2}s'),
                      delta=render_safe(scorecard_data['BLOCK_TIME_SECONDS__DELTA_30D'], '{:.1%}'),
                      delta_color="inverse", 
                      help=None, 
                      label_visibility="visible")

    chart_data = barchart_data[['UTC_DATE','BLOCK_TIME_SECONDS']]
    chart_data = chart_data.rename(columns={'UTC_DATE':'Date', 'BLOCK_TIME_SECONDS':'Seconds'})
    st.write()
    st.area_chart(data=chart_data, x='Date', y='Seconds',
                 use_container_width=True, height=500)

    
st.write('')
with st.container():
    st.subheader('Transactions per Second (TPS)')
    
    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours (Max)', 
                      value=render_safe(scorecard_data['MAX_TPS__PAST_24H'], '{:,.0f}'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days (Max)', 
                      value=render_safe(scorecard_data['MAX_TPS__PAST_7D'], '{:,.0f}'), 
                      delta=None, 
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days (Max)', 
                      value=render_safe(scorecard_data['MAX_TPS__PAST_30D'], '{:,.0f}'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        chart_data = barchart_data[['UTC_DATE','MAX_TPS']]
        chart_data = chart_data.rename(columns={'UTC_DATE':'Date', 'MAX_TPS':'TPS'})
        st.write('')
        st.line_chart(data=chart_data, x='Date', y='TPS',
                     use_container_width=True, height=500)
        
        
st.write('')
with st.container():
    st.subheader('Transaction Success Rate')

    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])

        with col2:
            st.metric(label='Past 24 Hours', 
                      value=render_safe(scorecard_data['SUCCESS_RATE__PAST_24H'],  '{:.1%}'),
                      delta=render_safe(scorecard_data['SUCCESS_RATE__DELTA_24H'], '{:.1%}'),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col3:
            st.metric(label='Past 7 Days', 
                      value=render_safe(scorecard_data['SUCCESS_RATE__PAST_7D'],  '{:.1%}'),
                      delta=render_safe(scorecard_data['SUCCESS_RATE__DELTA_7D'], '{:.1%}'),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Past 30 Days', 
                      value=render_safe(scorecard_data['SUCCESS_RATE__PAST_30D'],  '{:.1%}'),
                      delta=render_safe(scorecard_data['SUCCESS_RATE__DELTA_30D'], '{:.1%}'),
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

    chart_data = barchart_data[['UTC_DATE','SUCCESS_RATE']]
    chart_data['SUCCESS_RATE'] = chart_data['SUCCESS_RATE']*100
    chart_data = chart_data.rename(columns={'UTC_DATE':'Date', 'SUCCESS_RATE':'Success Rate (%)'})
    st.write('')
    st.area_chart(data=chart_data, x='Date', y='Success Rate (%)',
                  use_container_width=True, height=500)
