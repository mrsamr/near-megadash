import streamlit as st
import pandas as pd
import requests


st.set_page_config(
    page_title='Staking - NEAR Mega Dashboard', 
    page_icon='🪙',
    layout='wide'
)

def render_safe(value, format):
    try:
        x = format.format(value)
    except:
        x = None
    return x

@st.cache
def get_staking_data():
    url = 'https://node-api.flipsidecrypto.com/api/v2/queries/0c642aa3-528d-43ee-8eed-fbd6adc3ff96/data/latest'
    response = requests.get(url)
    data = response.json()
    return pd.DataFrame(data)

@st.cache
def get_validators_data():
    url = 'https://rpc.mainnet.near.org/'
    payload = {"method":"validators","params":[None],"id":123,"jsonrpc":"2.0"}
    response = requests.post(url, json=payload)
    data = response.json()
    validators_df = pd.DataFrame(data['result']['current_validators'])
    validators_df['stake'] = validators_df['stake'].astype('float')/1e24
    validators_df = validators_df.sort_values(by='stake', ascending=False)
    validators_df = validators_df.reset_index().drop('index', axis=1)
    validators_df = validators_df.assign(validator_type = lambda x: x['num_expected_blocks'].apply(lambda y: 'Block Producer' if y > 0 else 'Chunk-Only Producer'))
    validators_df['rank'] = validators_df.index+1
    return validators_df


staking_df = get_staking_data().copy()
current_near_supply = staking_df.sort_values(by='EPOCH_NUM', ascending=False).iloc[0].loc['TOTAL_NEAR_SUPPLY']
current_near_staked = staking_df.sort_values(by='EPOCH_NUM', ascending=False).iloc[0].loc['TOTAL_NEAR_STAKED']

validators_df = get_validators_data().copy()
block_producers_count = validators_df.query("validator_type=='Block Producer'").shape[0]
chunk_only_producers_count = validators_df.query("validator_type=='Chunk-Only Producer'").shape[0]
current_seat_price = round(validators_df['stake'].min(), 2)


st.title('🪙 Staking')

st.write('')
with st.container():
    st.subheader('Total and Staked Supply')
    
    with st.container():
        col1, col2, col3 = st.columns([2,3,3])
        
        with col2:
            st.metric(label='Total Supply (NEAR)', 
                      value=render_safe(current_near_supply/1e6,  '{:,.1f}M'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
            
        with col3:
            st.metric(label='Total Staked (NEAR)', 
                      value=render_safe(current_near_staked/1e6,  '{:,.1f}M'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
            
    chart_data = staking_df[['START_TIME','TOTAL_NEAR_STAKED','TOTAL_NEAR_SUPPLY']]
    chart_data['START_TIME'] = pd.to_datetime(chart_data['START_TIME'])
    chart_data = chart_data.rename(columns={'START_TIME':'Time', 'TOTAL_NEAR_STAKED':'Total Staked', 'TOTAL_NEAR_SUPPLY':'Total Supply'})
    st.write()
    st.line_chart(data=chart_data, x='Time', y=['Total Supply', 'Total Staked'],
                  use_container_width=True, height=500)


            
            
with st.container():
    st.subheader('Validators')
    
    with st.container():
        col1, col2, col3, col4 = st.columns([1,3,3,3])
        
        with col2:
            st.metric(label='Block Producers', 
                      value=render_safe(block_producers_count,  '{:,}'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
        
        with col3:
            st.metric(label='Chunk-Only Producers', 
                      value=render_safe(chunk_only_producers_count,  '{:,}'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")

        with col4:
            st.metric(label='Seat Price (NEAR)', 
                      value=render_safe(current_seat_price,  '{:,.2f}'),
                      delta=None,
                      delta_color="normal", 
                      help=None, 
                      label_visibility="visible")
            
    chart_data = validators_df[['account_id','stake','rank']].copy()
    chart_data['xlabel'] = chart_data['rank'].astype('str').str.rjust(4, ' ') + '. ' + chart_data['account_id']
    chart_data = chart_data.rename(columns={'xlabel':'Validator', 'stake':'Stake'})
    st.write()
    st.bar_chart(data=chart_data, x='Validator', y='Stake',
                 use_container_width=True, height=500)
    
