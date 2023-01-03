import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta


st.set_page_config(
    page_title='DeFi - NEAR Mega Dashboard', 
    page_icon='🏦',
    layout='wide'
)


def get_near_protocols():
    url = 'https://api.llama.fi/protocols'
    response = requests.get(url)
    protocols = response.json()
    near_protocols = [x for x in protocols if 'Near' in x['chains'] and x['category'] != 'CEX']
    return near_protocols

@st.cache
def get_defi_data():
    protocols_list = get_near_protocols()
    protocol_tvls = []
    token_tvls = []
    for p in protocols_list:
        try:
            slug = p['slug']
            url = f'https://api.llama.fi/protocol/{slug}'
            response = requests.get(url)
            data = response.json()
            tvl_df = pd.DataFrame(data['chainTvls']['Near']['tvl'])
            tvl_df['protocol'] = p['name']
            tvl_df['category'] = p['category']
            tvl_df['tvl_usd'] = tvl_df['totalLiquidityUSD']
            tvl_df['date'] = tvl_df['date'].apply(lambda x: datetime.utcfromtimestamp(x))
            tvl_df = tvl_df[['protocol','category','date','tvl_usd']]
            protocol_tvls.append(tvl_df)
            
            if p['category']=='Dexes':
                tokens_df = pd.concat([pd.DataFrame([{'date':x['date']} for x in data['tokensInUsd']]),
                                       pd.DataFrame([x['tokens'] for x in data['tokensInUsd']])], axis=1)
                tokens_df['date'] = tokens_df['date'].apply(lambda x: datetime.utcfromtimestamp(x))
                tokens_df = tokens_df.melt(id_vars='date', var_name='symbol', value_name='tvl_usd')
                tokens_df['protocol'] = p['name']
                token_tvls.append(tokens_df)
                
        except Exception as e:
            pass
        
    tvl_df_compiled = pd.concat(protocol_tvls, axis=0)
    token_tvl_df_compiled = pd.concat(token_tvls, axis=0)
    
    end_date = tvl_df_compiled['date'].max()
    start_date = end_date - timedelta(days=365)
    
    tvl_df_compiled = tvl_df_compiled.loc[tvl_df_compiled['date'] >= start_date]
    token_tvl_df_compiled = token_tvl_df_compiled.loc[token_tvl_df_compiled['date'] >= start_date]
    
    return tvl_df_compiled, token_tvl_df_compiled


tvl_data, token_tvl_data = get_defi_data()


st.title('🏦 Decentralized Finance')

st.write('')
with st.container():
    st.subheader('Total Value Locked')
    
    chart_data = tvl_data.copy()
    chart_data['rank'] = chart_data.index+1
    chart_data = chart_data.groupby(['date','category'], as_index=False).agg({'tvl_usd':'sum'})
    chart_data = chart_data.pivot_table(index='date', columns='category', values='tvl_usd', aggfunc='mean')
    chart_data = chart_data.reset_index()
    chart_data = chart_data.rename(columns={'date':'Date'})
    
    st.write('By Category')
    st.area_chart(data=chart_data, x='Date', y=[x for x in chart_data.columns if x != 'Date'],
                  use_container_width=True, height=500)
    
        
    chart_data = tvl_data.copy()
    chart_data = chart_data.pivot_table(index='date', columns='protocol', values='tvl_usd', aggfunc='mean')
    chart_data = chart_data.reset_index()
    chart_data = chart_data.rename(columns={'date':'Date'})
    
    st.write('By Protocol')
    st.area_chart(data=chart_data, x='Date', y=[x for x in chart_data.columns if x != 'date'],
                  use_container_width=True, height=500)

    
    st.subheader('Top DeFi Protocols')
    
    chart_data = tvl_data.copy()
    chart_data = chart_data.sort_values(by=['protocol','date'])
    chart_data = chart_data.groupby('protocol').tail(1)
    chart_data = chart_data.sort_values(by='tvl_usd', ascending=False)
    chart_data = chart_data.reset_index().drop('index', axis=1)
    chart_data['rank'] = chart_data.index+1
    chart_data['xlabel'] = chart_data['rank'].astype('str').str.rjust(3, ' ') + '. ' + chart_data['protocol'] + ' (' + chart_data['category'] + ')'
    chart_data['tvl_usd'] = chart_data['tvl_usd'].round(2)
    chart_data = chart_data.rename(columns={'tvl_usd':'TVL ($)', 'xlabel':'Protocol'})
    st.write()
    st.bar_chart(data=chart_data, x='Protocol', y='TVL ($)',
                 use_container_width=True, height=500)

    
    
    st.subheader('Top Tokens by Liquidity in DEXs')
    chart_data = token_tvl_data.copy()
    ref_finance_tokens = token_tvl_data.query("protocol=='Ref Finance'").symbol.unique()
    chart_data = chart_data.loc[chart_data['symbol'].isin(ref_finance_tokens)]
    chart_data = chart_data.dropna()
    chart_data['date'] = chart_data['date'].dt.date
    chart_data = chart_data.sort_values(by=['symbol','date','tvl_usd'], ascending=[False,False,False])
    chart_data = chart_data.groupby(['date','symbol','protocol'], as_index=False).head(1)
    chart_data = chart_data.groupby(['date','symbol'], as_index=False).agg({'tvl_usd':'sum'})
    chart_data = chart_data.sort_values(by=['symbol','date'], ascending=[False,False])
    chart_data = chart_data.groupby(['symbol'], as_index=False).head(1)
    chart_data = chart_data.sort_values(by='tvl_usd', ascending=False)
    chart_data = chart_data.reset_index().drop('index', axis=1)
    chart_data['tvl_usd'] = chart_data['tvl_usd'].round(2)
    chart_data['rank'] = chart_data.index+1
    chart_data['xlabel'] = chart_data['rank'].astype('str').str.rjust(3,' ') + '. ' + chart_data['symbol']
    chart_data = chart_data.rename(columns={'xlabel':'Token', 'tvl_usd':'TVL ($)'})
    
    st.bar_chart(data=chart_data, x='Token', y='TVL ($)',
                 use_container_width=True, height=500)
