import streamlit as st
from pathlib import Path
import pandas as pd
import numpy as np
import yfinance as yf
import altair as alt

description = """
Select at least 2 counters to compare their total gain over 10 years.
"""

st.header('Total Relative Return')

st.write(description)

stock_df = pd.read_csv('resources/sg_stocks_list.csv')
# stock_df.index = stock_df['Symbol']
stock_name = stock_df['Name']

options = st.multiselect('Your selection', stock_name)
filter = stock_df['Name'].isin(options)
selected_symbols = stock_df[filter]['Symbol'].to_list()

if len(selected_symbols) > 1:
    data = yf.download(selected_symbols, period='10y')
    data_closePrice = data['Adj Close']

    returns = data_closePrice.pct_change(1)
    log_returns = np.log(data_closePrice).diff()
    log_returns = log_returns.set_axis(options, axis=1)
    trr = 100*(np.exp(log_returns.cumsum()) - 1)

    trr_melt = trr.reset_index().melt(
        id_vars='Date',
        var_name='Counter',
        value_name='Total Relative Return (%)'
    )

    line = alt.Chart(trr_melt).mark_line().encode(
        x='Date',
        y='Total Relative Return (%)',
        color='Counter').properties(
        width=600,
        height=400
    ).configure_legend(
        orient='bottom',
        direction='vertical',
        offset=-380,
    )
    st.altair_chart(line)
