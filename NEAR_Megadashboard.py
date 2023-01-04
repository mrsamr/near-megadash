import streamlit as st

st.set_page_config(layout='wide')
st.title('NEAR Mega Dashboard')


intro_text = r"""
This app contains information and metrics on various parts of the NEAR ecosystem including:
- Blockchain activity
- Blockchain performance
- Staking and validators
- Decentralized finance

Please navigate to the different pages to view the information listed above.

---

**Data sources:**
1. Flipside Crypto
2. DefiLlama
3. NEAR RPC Node

---

*This app was originally developed as a contribution to MetricsDAO.*

"""

st.markdown(intro_text)


